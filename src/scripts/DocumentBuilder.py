import copy
import json
import os
from glob import glob

from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
from tqdm import tqdm

from utils.utils import save_docs_to_jsonl

text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=100, chunk_overlap=0
)


def club_captions(captions):
    clubbed_texts = []
    clubbed_starts = []

    for i, caption in enumerate(captions):
        start_time = caption["start"]
        duration = caption["duration"]
        end_time = start_time + duration

        for j in range(i + 1, len(captions)):
            next_start_time = captions[j]["start"]
            if next_start_time < end_time:
                clubbed_texts.append(caption["text"] + " " + captions[j]["text"])
                clubbed_starts.append(next_start_time)
            else:
                break

    return clubbed_texts, clubbed_starts


def build_document(handle_name, caption_paths, DOCUMENTS_PATH):
    try:
        documents = []
        for each_path in tqdm(caption_paths):

            video_id = os.path.basename(each_path).replace("_captions.jsonl", "")
            with open(each_path, "r") as video_caption_file:
                captions = []
                for line in video_caption_file:
                    data = json.loads(line)

                    text = data["text"]
                    data["text"] = text.encode("ascii", "ignore").decode()
                    captions.append(data)

            clubbed_texts, clubbed_starts = club_captions(captions)

            for clubbed_text, clubbed_start in zip(clubbed_texts, clubbed_starts):

                document = Document(
                    page_content=clubbed_text,
                    metadata={
                        "video_id": video_id,
                        "handle_name": handle_name,
                        "time": clubbed_start,
                    },
                )

                if len(clubbed_text) > 100:
                    splited_documents = text_splitter.split_documents(
                        documents=[document]
                    )
                    documents.extend(splited_documents)
                else:
                    documents.append(document)

        caption_document_path = save_docs_to_jsonl(
            documents, handle_name, DOCUMENTS_PATH
        )
        return caption_document_path
    except Exception as e:
        print(e)
        raise e

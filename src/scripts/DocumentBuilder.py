import os
from glob import glob

import copy
from tqdm import tqdm
import json
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
from utils.utils import save_docs_to_jsonl



text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=100, chunk_overlap=0
)

def build_document(DATASET_PATH, DOCUMENTS_PATH):
    try:
        paths = glob(DATASET_PATH + "*.jsonl")

        documents = []
        for each_path in tqdm(paths):
            video_id = os.path.basename(each_path).replace('_captions.jsonl', '')
            with open(each_path, 'r') as video_caption_file:
                for line in video_caption_file:
                    data = json.loads(line)

                    text = data['text']
                    string_encode = text.encode("ascii", "ignore")
                    text = string_encode.decode()
                    del data['text']
                    data['video_id'] = video_id

                    index = -1
                    for chunk in text_splitter.split_text(text):
                        metadata = copy.deepcopy(data)
                        
                        if text_splitter._add_start_index:
                            index = text.find(chunk, index + 1)
                            metadata["start_index"] = index
                        
                        new_doc = Document(page_content=chunk, metadata=metadata)
                        documents.append(new_doc)

        save_docs_to_jsonl(documents, DOCUMENTS_PATH)
        return True
    except Exception as e:
        print(e)
        return False
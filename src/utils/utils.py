import json
from uuid import uuid4

from langchain.docstore.document import Document


def save_docs_to_jsonl(documents, handle_name, DOCUMENTS_PATH):
    caption_document_path = (
        DOCUMENTS_PATH + f"{handle_name}_{uuid4().hex}_documents.jsonl"
    )
    with open(caption_document_path, "w") as jsonl_file:
        for doc in documents:
            jsonl_file.write(doc.json() + "\n")

    return caption_document_path


def load_docs_from_jsonl(handle_name, DOCUMENTS_PATH):
    documents = []
    with open(DOCUMENTS_PATH + f"{handle_name}_documents.jsonl", "r") as jsonl_file:
        for line in jsonl_file:
            data = json.loads(line)
            obj = Document(**data)
            documents.append(obj)
    return documents

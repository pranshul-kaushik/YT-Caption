from langchain.docstore.document import Document

import json

def save_docs_to_jsonl(documents, DOCUMENTS_PATH):
    with open(DOCUMENTS_PATH + 'documents.jsonl', 'w') as jsonl_file:
        for doc in documents:
            jsonl_file.write(doc.json() + '\n')

def load_docs_from_jsonl(DOCUMENTS_PATH):
    documents = []
    with open(DOCUMENTS_PATH + 'documents.jsonl', 'r') as jsonl_file:
        for line in jsonl_file:
            data = json.loads(line)
            obj = Document(**data)
            documents.append(obj)
    return documents

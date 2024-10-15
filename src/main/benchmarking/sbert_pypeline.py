import os
from sentence_transformers import SentenceTransformer, util
import fitz
import numpy as np

model = SentenceTransformer('all-mpnet-base-v2')


def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page_num in range(doc.page_count):
            page = doc[page_num]
            text += page.get_text("text")  # Extract plain text from each page
    return text


def read_txt_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


documents = {}
responses = {}
directory = "/Users/mmarfoi/Desktop/proiectDS/pythonProject/src/main/benchmarking"
for filename in os.listdir(directory):
    file_path = os.path.join(directory, filename)

    # If it's a PDF, extract text and store it
    if filename.endswith('.pdf'):
        doc_text = extract_text_from_pdf(file_path)
        documents[filename] = doc_text

    # If it's a response (txt file), store it
    elif filename.endswith('.txt'):
        response_text = read_txt_file(file_path)
        responses[filename] = response_text

# Convert documents to embeddings using SBERT
doc_embeddings = {}
for doc_name, doc_text in documents.items():
    doc_embeddings[doc_name] = model.encode(doc_text, convert_to_tensor=True)

results = {}
best_scores = []

for response_name, response_text in responses.items():
    response_embedding = model.encode(response_text, convert_to_tensor=True)
    response_results = {}

    # Compare the response against all documents
    max_score = -1  # Initialize a variable to track the best score for this response
    best_document = None

    for doc_name, doc_embedding in doc_embeddings.items():
        score = util.pytorch_cos_sim(response_embedding, doc_embedding).item()
        response_results[doc_name] = score

        if score > max_score:
            max_score = score
            best_document = doc_name

    best_scores.append(max_score)

    results[response_name] = {
        "best_document": best_document,
        "best_score": max_score,
        "all_scores": response_results
    }

for response_name, result in results.items():
    print(f"\nResponse: {response_name}")
    print(f"\tBest Match Document: {result['best_document']}, Best Similarity Score: {result['best_score']:.4f}")
    for doc_name, score in result['all_scores'].items():
        print(f"\tDocument: {doc_name}, Similarity Score: {score:.4f}")

mean_best_score = np.mean(best_scores)
print(f"\nAverage (mean) of best similarity scores: {mean_best_score:.4f}")

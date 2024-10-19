import os
import streamlit as st
import torch
from sentence_transformers import SentenceTransformer, util

# Load the pre-trained model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Function to load documents from .txt files in separate folders
def load_documents(root_dir):
    documents = []
    doc_paths = []
    # Traverse the directory to read all .txt files
    for folder in os.listdir(root_dir):
        folder_path = os.path.join(root_dir, folder)
        if os.path.isdir(folder_path):  # Ensure it's a directory
            for file_name in os.listdir(folder_path):
                if file_name.endswith('.txt'):  # Check if it's a text file
                    file_path = os.path.join(folder_path, file_name)
                    with open(file_path, 'r', encoding='utf-8') as file:
                        # Read the content of the text file
                        content = file.read()
                        documents.append(content)
                        doc_paths.append(file_path)
    return documents, doc_paths

# Function to load or create embeddings
def get_document_embeddings(documents):
    if os.path.exists('doc_embeddings.pt'):
        # Load precomputed embeddings if they exist
        doc_embeddings = torch.load('doc_embeddings.pt')
    else:
        # Otherwise, create embeddings and save them for future use
        doc_embeddings = model.encode(documents, convert_to_tensor=True)
        torch.save(doc_embeddings, 'doc_embeddings.pt')
    return doc_embeddings

# Define the path to the root directory containing the document folders
root_dir = 'citeseer2'

# Load documents from the folders
documents, doc_paths = load_documents(root_dir)

# Get or generate document embeddings
doc_embeddings = get_document_embeddings(documents)

# Streamlit app
st.title('Semantic Search for Documents')

# Input field for user query
query = st.text_input('Enter your search query:')

# Input field for the number of results
num_of_results = st.number_input('Enter the number of results:', min_value=1, max_value=100, value=5)

# Button to trigger search
if st.button('Search'):
    if query:
        # Encode the query
        query_embedding = model.encode(query, convert_to_tensor=True)

        # Compute cosine similarity between query and document embeddings
        cosine_scores = util.pytorch_cos_sim(query_embedding, doc_embeddings)[0]

        # Get the top results
        top_results = torch.topk(cosine_scores, k=num_of_results)

        # Display the results
        st.write(f"Top {num_of_results} results for '{query}':")
        for score, idx in zip(top_results.values, top_results.indices):
            st.write(f"Document {idx+1}: (Score: {score.item():.4f})")
            st.write(f"File Path: {doc_paths[idx]}")  # Show file path
            st.write(documents[idx][:500])  # Display the first 500 characters of the document
    else:
        st.warning("Please enter a query to search.")

import os
from sentence_transformers import SentenceTransformer
import torch

# Load the pre-trained model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Define the path to the directory containing folders with documents
root_dir = '/home/zhang3s2/workspace/8380/citeseer2'

# A list to store document contents
documents = []

# Iterate through each folder and read the text file
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

# Encode the document contents
print(f"Encoding {len(documents)} documents...")
doc_embeddings = model.encode(documents, convert_to_tensor=True)

# Save the embeddings to a file for future use (optional)
torch.save(doc_embeddings, 'doc_embeddings.pt')

print(f"Document embeddings shape: {doc_embeddings.shape}")

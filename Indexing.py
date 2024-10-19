import os
from whoosh.fields import Schema, TEXT, ID
from whoosh.index import create_in
from whoosh.analysis import StandardAnalyzer
from whoosh.writing import AsyncWriter

#Define the schema for the index
def create_schema():
    return Schema(
        path=ID(stored=True, unique=True),
        title=TEXT(stored=True),
        contents=TEXT(stored=True, analyzer=StandardAnalyzer())
    )

#Index all documents in a given directory
def index_docs(writer, docs_path):
    counter = 0
    for root, _, files in os.walk(docs_path):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding="utf-8") as f:
                title = f.readline().strip()  #First line as title
                contents = f.read()  #The rest of the file is content

                #Create a document and add fields
                writer.add_document(
                    path=file_path,
                    title=title,
                    contents=contents
                )
                counter += 1
                if counter % 1000 == 0:
                    print(f"Indexed {counter}-th file: {file}")
    print(f"Total files indexed: {counter}")

#Main function
def main(index_path, docs_path):
    if not os.path.exists(index_path):
        os.makedirs(index_path)

    #Create schema and index directory
    schema = create_schema()
    idx = create_in(index_path, schema)
    writer = AsyncWriter(idx)

    #Index the documents
    index_docs(writer, docs_path)

    #Commit changes
    writer.commit()
    print("Indexing completed.")

if __name__ == "__main__":
    #Update these paths as needed
    index_path = "C:/Users/atulp/Downloads/Dataset_IRS_index"
    docs_path = "C:/Users/atulp/Downloads/Dataset_IRS"
    
    print(f"Indexing files from {docs_path} to {index_path}...")
    main(index_path, docs_path)

import streamlit as st
from whoosh.index import open_dir
from whoosh.qparser import QueryParser

def search_indexed_docs(keywords, num_of_results):
    # Define the path to the index directory (you need to adjust this path)
    index_dir = "/home/zhang3s2/workspace/8380/index"
    
    # Open the index
    ix = open_dir(index_dir)
    
    # Create a searcher object
    with ix.searcher() as searcher:
        # Define the analyzer and parser for the search query
        parser = QueryParser("contents", ix.schema)
        query = parser.parse(keywords)

        # Perform the search, limit the results
        results = searcher.search(query, limit=num_of_results)
        
        # Prepare the results
        result_list = []
        for i, result in enumerate(results):
            result_dict = {
                "path": result['path'],
                "title": result.get('title')
            }
            result_list.append(result_dict)
        
        return result_list

# Streamlit app
st.title('Search Engine for Indexed Documents')

# Input fields for keywords and number of results
keywords = st.text_input('Enter keywords:')
num_of_results = st.number_input('Enter the number of results:', min_value=1, max_value=100, value=10)

# Button to trigger search
if st.button('Search'):
    if keywords:
        # Perform the search with the user inputs
        search_results = search_indexed_docs(keywords, num_of_results)
        
        # Display the results
        st.write(f"Found {len(search_results)} matching documents.")
        for i, result in enumerate(search_results):
            st.write(f"{i+1}. {result['path']}")
            if result['title']:
                st.write(f"   Title: {result['title']}")
    else:
        st.warning("Please enter some keywords to search.")

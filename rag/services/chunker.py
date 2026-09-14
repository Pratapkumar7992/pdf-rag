from langchain_text_splitters import RecursiveCharacterTextSplitter

def create_chunk(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
    )
    chunks = splitter.split_text(text)
    
    return chunks
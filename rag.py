import cohere
import chromadb
import os 
import dotenv
import PyPDF2
import numpy as np
import google.generativeai as genai
dotenv.load_dotenv()

genai.configure(api_key=os.environ.get('GEMINI')) 
def pdfchat(prompt, data):
    print(prompt)
    input = f"""
        You are a friendly AI bot. Your task is to respond the user's input.
        You can refer to the provided Data to respond to the user.
        If the Data is not relevant to the users input then respond based on your knowledge.
        USER: {prompt}
        Data: {data}
    """
    response = co.chat( 
    model='command-r',
    message=input,
    temperature=0.1,
    citation_quality='accurate',
    )
    print(response.text) 
    return response.text
    
    

cohere_api=os.environ.get('COHERE_API')
co = cohere.Client(cohere_api)
client = chromadb.Client()
collection = client.get_or_create_collection(name="main")


def db(text,embed,file_name,num):
    collection.add(
    documents=[text+" Source: "+file_name],
    embeddings=[embed],
    metadatas=[{"file_name": file_name}],
    ids=[file_name+" "+num]
    )

def embed(file, file_name):
    with open(file, 'rb') as f:
        pdf_reader = PyPDF2.PdfReader(f)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            response = co.embed(texts=[text], model='embed-multilingual-v3.0', input_type="search_document")
            embeddings = response.embeddings[0] 
            embeddings = np.array(response.embeddings[0]).astype(np.float64).tolist()   
            db(text, embeddings, file_name, str(page_num))
            print("uploaded "+ str(page_num))

def query_search(text):
    embedding=co.embed(texts=[text], model='embed-multilingual-v3.0', input_type="search_document")
    embedding=embedding.embeddings[0]
    embedding=np.array(embedding).astype(np.float64).tolist()
    try: 
        res=collection.query(
            query_embeddings=[embedding],
            n_results=5,
        )
        results = co.rerank(model="rerank-english-v2.0", query=text, documents=[str(res["documents"])], top_n=1)
        res=[]
        for result in results:
            document = result.document
            res.append(str(document))
        print(res)
        return res
    except:
        return "No relevant data found"
# def SearchWordPdf(query_str):
#     from whoosh.fields import ID,TEXT,Schema
#     import whoosh.index as index
#     from whoosh.fields import Schema,TEXT,ID
#     from whoosh.qparser import QueryParser
#     from whoosh.analysis import StemmingAnalyzer
#     import os
#     import docx2txt
#     import json
#     import PyPDF2
#     from spellchecker import SpellChecker
#     from nltk.corpus import stopwords
#     import re
    
#     # corrected all misspelled words from string
#     words = query_str.split()
#     spell = SpellChecker()
#     corrected = [spell.correction(word) for word in words]
    
#     # Remove stop words
#     stop_words = set(stopwords.words('english'))
#     query_str = [word for word in corrected if not word in stop_words]
#     query_str = " ".join(query_str)
    
#     directory_path = 'D:\\TFSApp\\KBHDataFiles\\KBHSolutions'
#     index_location = 'D:\\TFSApp\\KBHDataFiles\\KBHindex\\index'
#     time_file_path = 'D:\\TFSApp\\UTS\\pyKBH\\TimeFile\\time_file.txt'
    
#     schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT(stored=True,analyzer=StemmingAnalyzer()))

#     if not os.path.exists(index_location):
#         os.mkdir(index_location)
#         ix = index.create_in(index_location, schema)
#     else:
#         ix = index.open_dir(index_location)
        
#     def GetLastModifiedTime(directory_path):
#         x = os.path.getmtime(directory_path)
#         return x
    
#     def WriteLastModifiedTime(modified_time):
#         with open(time_file_path,'w') as f:
#             f.write(str(modified_time))
        
#     def ReadLastModifiedTimeFromFile():
#         with open(time_file_path,'r') as f:
#             previous_modified_time = float(f.read())
#         return previous_modified_time 
    
    
#     def CheckFileModifiedInDirectory():
#         temp = 0
#         modifiedtime = 0
#         newtime = 0
#         for filename in os.listdir(directory_path):
#             filepath = os.path.join(directory_path,filename)
#             if os.path.getmtime(filepath)>ReadLastModifiedTimeFromFile():
#                 modifiedtime = os.path.getmtime(filepath)
#                 if(newtime<=modifiedtime):
#                     newtime = modifiedtime
#                 temp = temp+1
#         if(temp==0):        
#             return False
#         else:
#             WriteLastModifiedTime(newtime)
#             return True
        
#     def CheckModifiedTime():
#         CheckTimeFile=os.path.exists(time_file_path)
#         if CheckTimeFile == False:
#             WriteLastModifiedTime(GetLastModifiedTime(directory_path))
#             return False
#         else:
#             if(CheckFileModifiedInDirectory()==True):
#                 return False
#             return True
    
#     if CheckModifiedTime()==False:
#         writer = ix.writer()
#         for root, dirs, files in os.walk(directory_path):
#             for file in files:
#                 if file.endswith(".docx"):
#                     text = docx2txt.process(os.path.join(root,file))
#                 elif file.endswith(".pdf"):
#                     with open(os.path.join(root,file),'rb') as f:
#                         pdf = PyPDF2.PdfReader(f)
#                         pages = len(pdf.pages)
#                         text = ''
#                         for page_number in range(pages):
#                             page = pdf.pages[page_number]
#                             text += page.extract_text ()
#                 else:
#                     continue
#                 writer.add_document(title=file,path=os.path.join(root,file),content=text)
#         writer.commit()
        
#     # region New Approach    
#     searcher = ix.searcher()
#     query = QueryParser("content", schema=ix.schema).parse(query_str)
#     with ix.searcher() as searcher:
#         results = searcher.search(query, limit=None)
#         results.fragmenter.charlimit = None
#         results.fragmenter.maxchars = 500                                                                                          
#         results.fragmenter.surround = 100
#         hits = []
#         relevant_para = []
#         for hit in results:
#             relevant_para.clear()
#             matched_para = re.sub('<.*?>', '', hit.highlights("content",top=4))
#             hits.append({"path":hit['path'],"paragraphs":matched_para.replace('\n','').replace('\t','')})
#         print(json.dumps(hits))
#     # endregion         
       
#     #region Old Approach    
#     # searcher = ix.searcher()
#     # query = QueryParser("content", schema=ix.schema).parse(query_str)
#     # results = searcher.search(query)
#     # hits  = []
#     # paths = []
#     # relevant_para = []
#     # for hit in results:
#     #     if hit['path'].endswith(".docx") or hit['path'].endswith(".pdf"):
#     #         relevant_para.clear()
#     #         paragraphs = hit["content"].split("\n")
#     #         for p in paragraphs:
#     #             if query_str.lower() in p.lower():
#     #                 relevant_para.append(p)
#     #                 if hit['path'] in paths:
#     #                     continue
#     #                 paths.append(hit['path'])
#     #         if len(relevant_para)>0:
#     #             hits.append({"path":hit['path'],"paragraphs":str(relevant_para).replace("]", "").replace("[", "").replace("\\t", "")})
#     # print(json.dumps(hits))
#     # endregion

# if __name__ == '__main__':
#     import sys
#     #SearchWordPdf(sys.stdin.readline().strip())
#     SearchWordPdf("shares")



# def SearchWordPdf(query_str):
#     from whoosh.fields import ID, TEXT, Schema
#     import whoosh.index as index
#     from whoosh.qparser import QueryParser
#     from whoosh.analysis import StemmingAnalyzer
#     import os
#     import docx2txt
#     import json
#     import PyPDF2
#     from spellchecker import SpellChecker
#     from nltk.corpus import stopwords
#     import re
#     import shutil
  
    
#     # Correct all misspelled words in the query string
#     words = query_str.split()
#     spell = SpellChecker()
#     corrected = [spell.correction(word) for word in words]


#     # Remove stop words
#     stop_words = set(stopwords.words('english'))
#     query_str = [word for word in corrected if word not in stop_words]
#     query_str = " ".join(query_str)

#     directory_path = 'D:\\TFSApp\\KBHDataFiles\\KBHSolutions\\Verified Solutions'
#     index_location = 'D:\\TFSApp\\KBHDataFiles\\KBHindex\\index'

#     schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT(stored=True, analyzer=StemmingAnalyzer()))

#     # Remove the existing index directory if it exists
#     if os.path.exists(index_location):
#         shutil.rmtree(index_location)

#     # Create the index directory
#     os.mkdir(index_location)
#     ix = index.create_in(index_location, schema)

#     writer = ix.writer()

#     # Indexing files
#     for root, dirs, files in os.walk(directory_path):
#         for file in files:
#             file_path = os.path.join(root, file)
#             if file.startswith('~$'):
#                 continue
#             try:
#                 if file.lower().endswith(".docx"):
#                     text = docx2txt.process(file_path)
#                 elif file.lower().endswith(".pdf"):
#                     with open(file_path, 'rb') as f:
#                         pdf = PyPDF2.PdfReader(f)
#                         pages = len(pdf.pages)
#                         text = ''
#                         for page_number in range(pages):
#                             page = pdf.pages[page_number]
#                             text += page.extract_text()
#                 else:
#                     continue
#                 writer.add_document(title=file, path=file_path, content=text)
#             except Exception as e:
#                 print(f"Failed to process {file_path}: {e}")
#                 continue

#     writer.commit()

#     # Search the index
#     searcher = ix.searcher()
#     query = QueryParser("content", schema=ix.schema).parse(query_str)
#     with ix.searcher() as searcher:
#         results = searcher.search(query, limit=None)
#         results.fragmenter.charlimit = None
#         results.fragmenter.maxchars = 500
#         results.fragmenter.surround = 100
#         hits = []
#         for hit in results:
#             matched_para = re.sub('<.*?>', '', hit.highlights("content", top=4))
#             hits.append({"path": hit['path'], "paragraphs": matched_para.replace('\n', '').replace('\t', '')})
#         print(json.dumps(hits, ensure_ascii=False, indent=4))  # Use ensure_ascii=False and indent for better formatting






# if __name__ == '__main__':
#     import sys
#     #SearchWordPdf("Add a New Vendor")
#     SearchWordPdf(sys.stdin.readline().strip())
from flask import Flask, request, jsonify
import json
import tempfile
import shutil
import os
import re
from azure.storage.blob import BlobServiceClient
from whoosh.index import create_in, open_dir, EmptyIndexError
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser
from whoosh.analysis import StemmingAnalyzer
import docx2txt
import PyPDF2

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, world!"
# Replace with your Azure Blob Storage connection string and container name
connection_string = 'DefaultEndpointsProtocol=https;AccountName=kbhdocumentstorage;AccountKey=doSuaslyxCWTQRhiKeyTQEIaT+wVsx4upRJmmNOicvGcb5vJCb1S5d+0bsNQitQxI4uVbYtTwcT1+AStUfrp0Q==;EndpointSuffix=core.windows.net'
container_name = 'kbhdocumentcontainer'

def create_index_and_upload(connection_string, container_name):
    # Define the schema for the index
    schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT(stored=True, analyzer=StemmingAnalyzer()))

    # Create a temporary directory for the index on local machine
    temp_index_dir = tempfile.mkdtemp()

    try:
        # Create the index
        ix = create_in(temp_index_dir, schema)
        writer = ix.writer()

        # Connect to Azure Blob Storage
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        container_client = blob_service_client.get_container_client(container_name)

        # Iterate through blobs in the container
        for blob in container_client.list_blobs():
            blob_client = container_client.get_blob_client(blob.name)

            # Skip system files or non-documents
            if blob.name.startswith('~$') or not (blob.name.lower().endswith(".docx") or blob.name.lower().endswith(".pdf")):
                continue

            try:
                # Download blob content
                with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                    download_stream = blob_client.download_blob()
                    temp_file.write(download_stream.readall())
                    temp_file_path = temp_file.name

                # Extract text from document based on file type
                if blob.name.lower().endswith(".docx"):
                    text = docx2txt.process(temp_file_path)
                elif blob.name.lower().endswith(".pdf"):
                    with open(temp_file_path, 'rb') as f:
                        pdf = PyPDF2.PdfReader(f)
                        text = ""
                        for page in pdf.pages:
                            text += page.extract_text()

                # Add document to the index
                writer.add_document(title=blob.name, path=blob_client.url, content=text)

                # Clean up temporary file
                os.remove(temp_file_path)

            except Exception as e:
                print(f"Failed to process {blob.name}: {e}")

        writer.commit()

        # Upload index files to Azure Blob Storage
        for root, _, files in os.walk(temp_index_dir):
            for file in files:
                local_file_path = os.path.join(root, file)
                blob_name = os.path.relpath(local_file_path, temp_index_dir).replace("\\", "/")  # Azure Blob Storage uses forward slashes
                blob_client = container_client.get_blob_client(blob_name)
                
                with open(local_file_path, "rb") as data:
                    blob_client.upload_blob(data, overwrite=True)

    finally:
        # Clean up local temp index directory
        shutil.rmtree(temp_index_dir)

def download_index_from_blob(connection_string, container_name, temp_index_dir):
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)

    # Ensure the temporary directory exists or create it
    os.makedirs(temp_index_dir, exist_ok=True)

    try:
        # Download index files from Azure Blob Storage
        for blob in container_client.list_blobs():
            blob_client = container_client.get_blob_client(blob)
            download_file_path = os.path.join(temp_index_dir, blob.name)
            os.makedirs(os.path.dirname(download_file_path), exist_ok=True)
            with open(download_file_path, "wb") as download_file:
                download_file.write(blob_client.download_blob().readall())

    except Exception as e:
        print(f"Failed to download index files: {e}")
        raise

def search_index(query_str, connection_string, container_name, temp_index_dir):
    try:
        # Download index files from Azure Blob Storage
        download_index_from_blob(connection_string, container_name, temp_index_dir)

        # Open index from downloaded files
        ix = open_dir(temp_index_dir)
        searcher = ix.searcher()
        query = QueryParser("content", schema=ix.schema).parse(query_str)

        # Perform search
        results = searcher.search(query, limit=None)
        hits = []
        for hit in results:
            matched_para = re.sub('<.*?>', '', hit.highlights("content", top=4))
            hits.append({"path": hit['path'], "paragraphs": matched_para.replace('\n', '').replace('\t', '')})

        searcher.close()
        ix.close()

        return hits

    except EmptyIndexError as e:
        print(f"EmptyIndexError: {e}")

    finally:
        # Clean up local temp index directory
        try:
            shutil.rmtree(temp_index_dir)
        except Exception as e:
            print(f"Failed to delete temporary index directory: {e}")


@app.route('/search', methods=['GET'])
def search():
    query_str = request.args.get('q', '')

    # Create a temporary directory for the index on local machine
    temp_index_dir = tempfile.mkdtemp()

    try:
        # Search the index on Azure Blob Storage
        results = search_index(query_str, connection_string, container_name, temp_index_dir)
        return jsonify(results)

    finally:
        # Clean up local temp index directory
        try:
            shutil.rmtree(temp_index_dir)
        except Exception as e:
            print(f"Failed to delete temporary index directory: {e}")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
# import os
# from flask import Flask

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return "Hello, world!"

# if __name__ == '__main__':
#     port = int(os.environ.get('PORT', 8000))
#     app.run(host='0.0.0.0', port=port)

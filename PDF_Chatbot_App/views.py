from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect
from django.core.files.storage import default_storage, FileSystemStorage
from django.conf import settings
import openai
import json
import os
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
import re
import fitz
import tiktoken
import requests

# <----------------------------------------------------- Config API keys/endpoints ------------------------------------------------------> 

# Configure OpenAI settings
openai.api_type = "azure"
openai.api_version = "2023-07-01-preview"
openai.api_base = getattr(settings, 'OPENAI_API_BASE')
openai.api_key = getattr(settings, 'OPENAI_API_KEY')
model_id = 'gpt-4-turbo-1106p'

# Configure Azure Document Analysis settings
endpoint = getattr(settings, 'DI_API_ENDPOINT')
key = getattr(settings, 'DI_API_KEY')



# <----------------------------------------------------- Rendering functions ------------------------------------------------------> 

def french(request):
    """
    Renders the home page for the chat application.
    """
    return render(request, 'french.html')
    
def overview(request):
    """
    Renders the overview page of the application.
    """
    return render(request, 'overview.html')

def chat(request):
    """
    Renders the chat page, passing the URL of the uploaded PDF if available.
    """
    uploaded_pdf_url = request.session.get('uploaded_pdf_url', '')
    return render(request, 'chat.html', {'uploaded_pdf_url': uploaded_pdf_url})

def banner_image(request):
    image_path = os.path.join(settings.BASE_DIR, 'imgs', 'banner.jpg')
    with open(image_path, 'rb') as f:
        return HttpResponse(f.read(), content_type="image/jpeg")

# <----------------------------------------------------- Doc Processing Functions ------------------------------------------------------> 
 
def get_content(file):
    """
    Extracts and refines the content of a document using Document Intelligence.

    Steps:
    - Initialize the client with endpoint and key.
    - Open the file in binary mode and analyze the document.
    - Extract the content and refine it using the 'refine_content' function.
    - Handle exceptions and return the refined content.
    """
    refined_content = ""  
    try:  
        # Open the PDF file  
        document = fitz.open(file)  
          
        # Initialize a variable to store the extracted text  
        text = ""  
  
        # Iterate over each page and extract text  
        for page_num in range(len(document)):  
            page = document.load_page(page_num)  
            text += page.get_text()  
  
        # Close the document  
        document.close()  

        return re.sub(r'\s+', ' ', text) 
  
    except Exception as e:  
        print(f"Error processing document: {e}")  
        return None   
      
    # Append a marker to indicate the end of the document content.  
    # refined_content += "\n-- End of Document --" 

    # Document Intelligence option - there is a model for just text extraction if it is ever needed
    client = DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    try:
        # Open the file and analyze it.
        with open(file, 'rb') as f:
            poller = client.begin_analyze_document("prebuilt-read", document=f)
            result = poller.result()
            content = result.content
            # refined_content = refine_content(result)
    except Exception as e:
        print(f"Error processing document: {e}")
    # # Append a marker to indicate the end of the document content.
    # refined_content += ""
    return content

def get_content_raw(file):
    """
    Extracts and refines the content of a document using Document Intelligence.

    Steps:
    - Initialize the client with endpoint and key.
    - Open the file in binary mode and analyze the document.
    - Extract the content and refine it using the 'refine_content' function.
    - Handle exceptions and return the refined content.
    """
    link = "https://ringtail-tops-hopelessly.ngrok-free.app"
    try:
        # Open the file and analyze it.
        with open(file, 'rb') as f:
            doc =f

            
        
            
        
    except Exception as e:
        print(f"Error processing document: {e}")

    return requests.post(link+'/translate', json={"engtext": doc}).json()['output']



def refine_content(result):
    """
    Refines the content extracted from a document into a structured JSON format.

    Steps:
    - Iterate through paragraphs and tables in the document.
    - For each, extract relevant details (content, page numbers, cell content, etc.).
    - Convert the structured data into JSON format.
    - Print and return the JSON string.
    """
    refined_data = {
        "Paragraphs": [
            {
                "Content": paragraph.content,
                # Safely access the page number if available.
                "PageNumber": paragraph.bounding_regions[0].page_number if paragraph.bounding_regions else "N/A"
            }
            for paragraph in result.paragraphs
        ],
        "Tables": [
            {
                "RowCount": table.row_count,
                "ColumnCount": table.column_count,
                "Cells": [{"Content": cell.content} for cell in table.cells]
            }
            for table in result.tables
        ]
    }
    # Convert the structured data into a formatted JSON string.
    refined_json = json.dumps(refined_data, indent=4)
    # Check the json output 
    print(refined_json)  
    return refined_json

# <----------------------------------------------------- Front End Connecting Functions ------------------------------------------------------> 

def upload_document(request):
    """
    Processes document uploads. Accepts only PDF files.

    Steps:
    - Check if the request method is POST and there's a file uploaded.
    - Save the uploaded PDF file using FileSystemStorage.
    - Extract text from the uploaded document.
    - Redirect to the chat page with the extracted text stored in the session.
    - Handle invalid uploads with an error message.
    """
    if request.method == 'POST':
        # Attempt to retrieve the uploaded file from the request.
        uploaded_file = request.FILES.get('document')
        # Ensure the file is a PDF before proceeding.
        if uploaded_file and uploaded_file.name.lower().endswith('.pdf'):
            # Save the uploaded file using Django's file system storage.
            fs = FileSystemStorage()
            filename = fs.save(uploaded_file.name, uploaded_file) # Note this will stay stored in the web app, TODO: add remove of old documents
            uploaded_file_url = fs.url(filename)
            # Store the URL of the uploaded file in the session.
            request.session['uploaded_pdf_url'] = uploaded_file_url
 
            full_temp_path = os.path.join(fs.location, filename)
            extracted_text = get_content(full_temp_path)
            print(f"extracted content: {extracted_text}")
            # Store the extracted document content in the session.
            request.session['document_content'] = extracted_text

            # Redirect the user to the chat page after successful upload and processing.
            return redirect('chat')
        else:
            # Return an error response if the uploaded file is not a valid PDF.
            return HttpResponseBadRequest("Please upload a valid PDF file.")
    else:
        # If the request method is not POST, render the chat home page.
        return render(request, 'chat_home.html')


 
@require_http_methods(["GET", "POST"])
def chatbot_view(request):
    """
    Handles chat interactions with the OpenAI API.

    POST: Processes a new message, updates chat history, and responds with status.
    GET: Streams responses from OpenAI based on the chat history and document content.
    """
    if request.method == 'POST':
        # Parse the incoming JSON data from the request body.
        data = json.loads(request.body)
        new_message = data.get('chatHistory')

        chat_history = request.session.get('chat_history', [])
        chat_history.append({"role": "user", "content": new_message})
        request.session['chat_history'] = new_message

        return JsonResponse({'status': 'success'}) 
    elif request.method == 'GET':
        chat_history = request.session.get('chat_history', [])
        document_content = request.session.get('document_content', '')
        return StreamingHttpResponse(request_translate_response(document_content), content_type='text/event-stream')
    
def num_tokens_from_string(string) -> int:
    encoding = tiktoken.get_encoding('cl100k_base')
    num_tokens = len(encoding.encode(string))
    return num_tokens


# <----------------------------------------------------- AI API Call Functions ------------------------------------------------------> 

def request_openai_response(chat_history, document_content):
    """
    Streams responses from OpenAI for the chat view. 

    - Formats the chat history and document content for the OpenAI API.
    - Sends the formatted data to OpenAI and yields responses as they are received.
    - Handles exceptions and yields error messages if necessary.
    """
    messages = [{
        "role": "system","content": "You are a helpful assistant that ALWAYS responds in consistent and pleasing HTML formatted text. Also, make sure to use borders ONLY IF you use a table in your response. Only answer the LAST QUESTION based on the document provided. Do not answer any questions not related to the document or PDF. Also, at the end of the entire total response tell me what pages you found the information on separated by commas. For example, at the end include: Source_page: <page-number1, page-number2, etc>." + document_content
    }]
    messages.extend(chat_history)
    new_message_string = json.dumps(messages)
    tokens_used = num_tokens_from_string(new_message_string)
    tokens_used
    print(tokens_used)
    try:
        stream = openai.ChatCompletion.create(
            engine=model_id,
            messages=messages,
            temperature=0.3,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None,
            stream=True
        )
        for response in stream:
            #print(response)
            data = json.dumps({'content': response, 'tokens_used': tokens_used})
            yield f"data: {data}\n\n"
    except Exception as e:
        yield f"data: {{'error': 'Error fetching data from OpenAI: {str(e)}'}}\n\n"

def request_translate_response(document_content):
    try:
        link = "https://ringtail-tops-hopelessly.ngrok-free.app"

        print(document_content)
        r = requests.post(link+'/translate', json={"engtext": document_content})
        
        data = json.dumps({'translation': r.json()['output']})
        print(data)
        yield data
    except Exception as e:
        yield f"data: {{'error': 'Error fetching data from API: {str(e)}'}}\n\n"
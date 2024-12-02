from django.conf import settings 
import openai 
from azure.ai.formrecognizer import DocumentAnalysisClient

# Configure OpenAI settings
openai.api_type = "azure"
openai.api_version = "2024-05-01-preview"
openai.api_base = getattr(settings, 'OPENAI_API_BASE')
openai.api_key = getattr(settings, 'OPENAI_API_KEY')
model_id = 'gpt-4-turbo'

# Define the path to the document file
document_file_path = "test.txt"

# Reads in txt document contents
def read_document(file_path):
    with open(file_path, "r", encoding="utf8") as file:
        doc_content = file.read()
    return doc_content

# Creates prompt that has the context of a document's content
def add_doc_to_prompt(doc_content, input):
    # print("add_doc_to_prompt called")
    chat_input = "Read the following document:" + doc_content + "\n\n" + 'User: ' + input + '\n'
    return chat_input

# Uses OpenAI API to answer user prompts.
def chat_with_openai_api(conversation_input):
    response = openai.ChatCompletion.create(
          engine=model_id,  
          messages= conversation_input,  
          temperature=0.2,  
          frequency_penalty=0,  
          presence_penalty=0,  
          stop=None,  
          stream=False  
    )

    print(response)
    print("Token usage:", response["usage"]["total_tokens"])
    return response.choices[0].message.content



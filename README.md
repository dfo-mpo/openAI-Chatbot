# DFO OpenAI Tool Suite

## Description
The DFO OpenAI Tool Suite is a web application equipped with a suite of AI tools designed for document interaction and analysis. This application enables users to leverage powerful AI capabilities directly through their web browser. Built using Django, Python, CSS, HTML, and JavaScript, this suite is well-suited for both individuals and businesses.

## Tools Included
- **AI ChatBot**: Allows real-time conversations with PDF documents, making it suitable for general inquiries and simple prompts.
- **CSV/PDF Analyzer**: Analyzes and extracts information from PDF documents by uploading the document along with a CSV file containing engineered prompts.
- **Sensitivity Score Calculator**: Computes the sensitivity level of uploaded documents based on custom parameters.
- **Redactor**: Scans and redacts specific information from uploaded PDF documents.

## Prerequisites
Before you begin the setup process, make sure to install the following:
- Python 3.9
- pip (Python package installer)

## Setup Instructions

### 1. Install Python
Download and install Python 3.9 from the official website:
[Python Downloads](https://www.python.org/downloads/)
During installation, ensure to check the box that says 'Add Python 3.9 to PATH'.

### 2. Clone the Repository
Clone the repository to your local machine with the following command:
```bash
git clone https://github.com/dfo-mpo/openAI-Chatbot.git
cd openAI-Chatbot
```
### 3. Install Dependencies
Install all required dependencies by running the following command in the project directory:
```bash
pip install -r requirements.txt
```
### 4. Set Up Environment Variables
Create a .env file in the root directory of your project and populate it with necessary API keys and other sensitive configurations:
```bash
OPENAI_API_KEY = ""
OPENAI_API_ENDPOINT = ""

BLOB_CONNECTION_STR = ""
BLOB_CONTAINER_NAME = ""

openai.api_type = ""
OPENAI_API_BASE = ""

 
DI_API_ENDPOINT = ""
DI_API_KEY = ""
```
For API key configuration, refer to the instructions available at SharePoint Link (placeholder).

### 5. Run the Application
Start the local server by running:
```bash
python manage.py runserver
```
You can access the web application by visiting http://127.0.0.1:8000 in your web browser.

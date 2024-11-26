from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import openai
from django.shortcuts import render, redirect
import json
from django.core.files.storage import default_storage
from django.http import HttpResponseBadRequest
from pypdf import PdfReader
import os
import io
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
import re
from pdfminer.high_level import extract_text
from presidio_analyzer import AnalyzerEngine
import fitz  
import requests
import numpy
from PIL import Image

def banner_image(request):
    image_path = os.path.join(settings.BASE_DIR, 'imgs', 'banner.jpg')
    with open(image_path, 'rb') as f:
        return HttpResponse(f.read(), content_type="image/jpeg")

def home(request):
    return render(request, 'home.html')

def fence(request):

    fs = FileSystemStorage()
    # Sample 1
    sample_name = 'Chinook-9s.jpg'
    filename = os.path.join('cached_outputs', sample_name)
    example_file_url = fs.url(filename)
    request.session['sample1_mp4_thumbnail_url'] = example_file_url
    # Strip the .jpg extension and add .pdf  
    pdf_name = sample_name.rsplit('.', 1)[0] + '.mp4'  
    request.session['sample1_mp4_name_url'] = pdf_name

    # Sample 2
    sample_name = 'Sockeye-2s.jpg'
    filename = os.path.join('cached_outputs', sample_name)
    example_file_url = fs.url(filename)
    request.session['sample2_mp4_thumbnail_url'] = example_file_url
    # Strip the .jpg extension and add .pdf  
    pdf_name = sample_name.rsplit('.', 1)[0] + '.mp4'  
    request.session['sample2_mp4_name_url'] = pdf_name

    # Sample 3
    # sample_name = 'Chum_SCL_2001_03.png'
    # filename = os.path.join('cached_outputs', sample_name)
    # example_file_url = fs.url(filename)
    # request.session['sample3_tif_thumbnail_url'] = example_file_url
    # # Strip the .jpg extension and add .pdf  
    # pdf_name = sample_name.rsplit('.', 1)[0] + '.tif'  
    # request.session['sample3_tif_name_url'] = pdf_name
    return render(request, 'fence.html')

def scale(request):

    fs = FileSystemStorage()
    # Sample 1
    sample_name = 'Chum_SCL_2001_01.png'
    filename = os.path.join('cached_outputs', sample_name)
    example_file_url = fs.url(filename)
    request.session['sample1_tif_thumbnail_url'] = example_file_url
    # Strip the .jpg extension and add .pdf  
    pdf_name = sample_name.rsplit('.', 1)[0] + '.tif'  
    request.session['sample1_tif_name_url'] = pdf_name

    # Sample 2
    sample_name = 'Chum_SCL_2001_02.png'
    filename = os.path.join('cached_outputs', sample_name)
    example_file_url = fs.url(filename)
    request.session['sample2_tif_thumbnail_url'] = example_file_url
    # Strip the .jpg extension and add .pdf  
    pdf_name = sample_name.rsplit('.', 1)[0] + '.tif'  
    request.session['sample2_tif_name_url'] = pdf_name

    # Sample 3
    sample_name = 'Chum_SCL_2001_03.png'
    filename = os.path.join('cached_outputs', sample_name)
    example_file_url = fs.url(filename)
    request.session['sample3_tif_thumbnail_url'] = example_file_url
    # Strip the .jpg extension and add .pdf  
    pdf_name = sample_name.rsplit('.', 1)[0] + '.tif'  
    request.session['sample3_tif_name_url'] = pdf_name

    return render(request, 'scale.html')

     
def french(request):
    return render(request, 'french.html')
    
def overview(request):
    return render(request, 'overview.html')

def calculate_sensitivity_score(analyzer_results):
    weights = {
        'PERSON': 0.05,
        'LOCATION': 0.05,
        'DATE_TIME': 0.02,
        'ORGANIZATION': 0.1,
        'PHONE_NUMBER': 0.3,
        'EMAIL_ADDRESS': 0.3,
        'CREDIT_CARD': 1.0,
        'NATIONAL_ID': 1.0,
    }
    score = sum(weights.get(result.entity_type, 0) * 100 for result in analyzer_results)  # Convert to percentage
    return min(score, 100)  # Ensure the score does not exceed 100%

# Function to perform PII recognition using Presidio
def pii_recognition_example(pdf_path):
    analyzer = AnalyzerEngine()

    # Extract text from PDF
    text = extract_text(pdf_path)

    # Analyze the text for PII using Presidio
    analyzer_results = analyzer.analyze(text=text, language='en')

    # Calculate sensitivity score
    sensitivity_score = calculate_sensitivity_score(analyzer_results)

    return sensitivity_score



# Function to perform the sensitivity analysis
def analyze_sensitivity(request):
    if request.method == 'POST':
        if 'example_document' in request.POST:
            fs = FileSystemStorage()
            filename = os.path.join('cached_outputs', request.POST.get('example_document'))
            document_path = fs.path(filename)

            # Create a URL for the PNG file  
            png_filename = f"{filename.rsplit('.', 1)[0]}.png" 
            png_url = fs.url(png_filename)  

        else:
            uploaded_file = request.FILES['document']
            fs = FileSystemStorage()
            filename = fs.save(uploaded_file.name, uploaded_file) # Note this will stay stored in the web app, TODO: add remove of old documents
            document_path = fs.path(filename)

            # Open the TIFF file and convert it to PNG  
            image = Image.open(document_path)  
            npimg = numpy.array(image)  
            listimg = npimg.tolist()  
    
            # Convert image to PNG  
            png_image_io = io.BytesIO()  
            image.save(png_image_io, format='PNG')  
            png_image_io.seek(0)  
          
            # Store PNG image in session or save to file system  
            png_filename = f"{filename.rsplit('.', 1)[0]}.png"  
            fs.save(png_filename, png_image_io)  

            # Create a URL for the PNG file  
            png_url = fs.url(png_filename)   
            request.session['uploaded_png_url'] = png_url
            print(png_url)

        # Extract list from array from image
        image = Image.open(document_path)
        npimg = numpy.array(image)
        listimg = npimg.tolist()
        apilink = "https://www.example.com"

        r = requests.post("https://ringtail-tops-hopelessly.ngrok-free.app/scale", verify=False, json={"imagelist": listimg})
        print("Age predicted: ", r)
        print(r.json()['output'])
        return JsonResponse({"output": r.json()['output'], "uploaded_name": png_filename, "png_url": png_url})



def upload_video(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('document')
        if uploaded_file and uploaded_file.name.lower().endswith(('.mp4', '.avi')):
            fs = FileSystemStorage()
            
            # Split the filename and extension
            name, extension = os.path.splitext(uploaded_file.name)
            # Define the new filename with '-redacted' appended
            # new_filename = f"{name}-analyzed{extension}"
            new_filename = os.path.join('cached_outputs', f"{name}.mp4")

            # Check if the file does not already exist
            filename = uploaded_file.name
            if not fs.exists(uploaded_file.name):
                # Save the original file
                filename = fs.save(uploaded_file.name, uploaded_file)
            
            # Define the output path with the new filename
            processed_path = os.path.join(fs.location, new_filename)
            
            # Call your redaction function here
            # redact_pdf_based_on_pii(document_path, processed_path)

            # # Make sure to delete the original file
            # os.remove(full_temp_path)

            # Store paths or videos in memory
            original_video_url = fs.url(filename)
            processed_video_url = fs.url(new_filename)
            print(processed_video_url)
            # request.session['uploaded_video_url'] = original_video_url
            # request.session['processed_video_url'] = processed_video_url
            
            return JsonResponse({'processedVideoURL': processed_video_url, 'uploadedVideoURL': original_video_url})
        else:
            return HttpResponseBadRequest("Please upload a valid video file.")

 
 

 
 
def redact_pdf_based_on_pii(pdf_path, output_pdf_path):
    """
    Redacts specific PII types in a PDF file.
    
    :param pdf_path: Path to the input PDF file.
    :param output_pdf_path: Path where the redacted PDF will be saved.
    """
    # Initialize Presidio Analyzer
    analyzer = AnalyzerEngine()

    # Define PII entities to redact
    entities_to_redact = [
        'PERSON', 'PHONE_NUMBER', 'EMAIL_ADDRESS', 
        'CREDIT_CARD', 'IBAN', 'US_BANK_NUMBER', 
        'DATE_TIME', 'NATIONAL_ID', 'SSN'
    ]

    # Open the PDF
    doc = fitz.open(pdf_path)
    
    for page in doc:
        text = page.get_text("text")
        analyzer_results = analyzer.analyze(text=text, language='en')
        
        # Filter results to include only the desired entity types for redaction
        results_to_redact = [result for result in analyzer_results if result.entity_type in entities_to_redact]
        
        for result in results_to_redact:
            # Search for the text of each result to get the position for redaction
            spans = page.search_for(text[result.start:result.end])
            for span in spans:
                # Add redaction annotation
                page.add_redact_annot(span, fill=(0, 0, 0))  # Use black color to redact

        # Apply the redactions
        page.apply_redactions()

    # Save the redacted PDF
    doc.save(output_pdf_path, garbage=4, deflate=True)
    doc.close()

 


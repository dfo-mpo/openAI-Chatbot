# Frontend Image Logic
## Framework/Structure 
The frontend component is a React JS project located under `./src`. This component creates an interface where users interact with the OCDS E-AI Hub and its various tools.  

The frontend component does not have its own direct backend and processing any of the hosted tools is done by making requests to the server and backend components. 

Using a terminal shell, the frontend can be started by simply using the `npm run dev` command (which also starts up the server component). When using Docker, it is deployed as its own container. In this case, it is packaged with a nginx that servers as a reverse proxy. 

All dependencies used in this component are defined in the `package.json` and `package-lock.json` files. 

## Communicating with tool APIs 
All requests made to in house APIs (hosted in an Azure Shared Services Canada environment) are handled in the `/services/apiService.js` file using helper functions called by various tool pages needing the API. 

## Authenticating Users into the Platform 
### Authentication Overview 
User authentication within the OCDS E-AI Hub frontend is implemented using Microsoft Entra ID through the Microsoft Authentication Library (MSAL) for Reach. 

The implementation follows Microsoft’s official guidance for React-based Page Applications (SPA):  
- [Get started with MSAL React - Microsoft Authentication Library for JavaScript | Microsoft Learn](https://learn.microsoft.com/en-us/entra/msal/javascript/react/getting-started?view=msal-js-latest)
- [Tutorial: Prepare a React single-page application for authentication - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/tutorial-single-page-app-react-prepare-app?tabs=workforce-tenant)

The application uses the `@azure/msal-react` and `@azure/msal-browser` packages to handle authentication requests. 

### Prerequisites 
Authentication requires a registered application in Microsoft Entra ID configured as 
- Application type: Single Page Application (SPA) 
- Platform configuration: Redirect URI configured for the deployed URL 

The `Client ID` and `Tenant ID` are configured in the frontend authentication configuration file. 

### Configuration Structure 
MSAL configuration is defined in `src\components\auth\authConfig.js`. 

This configuration follows the structure provided in the MSAL React documentation, with environment specific credentials. The configuration initializes an MSAL instance used across the application. 

### Application Integration 
MSAL is integrated at the root of the React application. In `./src/App.js`, the application is wrapped in: 
- MsalProvider: provides authentication context across the component 
- AuthContext: custom lightweight wrapper used to simplify authentication state checks within UI components 

This design allows authentication state to be accessed globally without tightly coupling components to MSAL specific hooks. 

Authentication state is exposed via `AuthContext`, and UI components consume authentication state via `useAuth()`. 

### Login Behavior and Access Control Model 
The OCDS E-AI Hub does not enforce mandatory login on initial page load. Instead, it fllows a conditional access visibility model: 
- Users may browse publicly accessible content without authentication. 
- Certain components and features remain restricted until the user is authenticated. 
- When unauthenticated, a login button is displayed in the header; if authenticated, the login button is replaced by logout functionality. 

## Language Toggling 
Due to the unreliability of automatic translation tools/libraries especially in a DFO context; a custom built in tool is used for toggling language between English and French. Each piece of English text needs to have a French translation (acquired manually) in a structured object in the `translations/` folder. Each page in the OCDS E-AI Hub then needs to use these defined objects in place of any text, so what is generated depends on the current language selected. 

When the language toggle button is used, the `contexts/LanguageContext.js` file is used by the toggle and all OCDS E-AI Hub pages to keep track of what the current language is. 

## Google Analytics 
Google Analytics has been setup to track various events and pages in the OCDS E-AI Hub to better understand user behavior. The `react-ga4` library is used in the file `src/utils/analytics.js` to set up helper functions to track page views and specific events. It is then called in `src/App.js` to initialize the Google Analytics connection and page tracking. Any page in the OCDS E-AI Hub can then track specific events by importing `trackEvent()` from `analytics.js` and calling it during an event (such as a button click or API request failure). The name of the tool, description of the event, and label of the event type should always be passed to the `trackEvent()` function. 

For documentation on setting up and tracking events in a Google Analytics workspace see the document [How to Track Web App Traffic Using Google Analytics 4.docx](https://086gc.sharepoint.com/:w:/r/sites/PacificSalmonTeam/Shared%20Documents/General/02%20-%20PSSI%20Secretariat%20Teams/04%20-%20Strategic%20Salmon%20Data%20Policy%20and%20Analytics/10%20-%20Documentation/01%20-%20Data%20Analytics%20Team/08%20-%20Google%20Analytics/How%20to%20Track%20Web%20App%20Traffic%20Using%20Google%20Analytics%204.docx?d=w3290d776fea34e8d916826fe338dd091&csf=1&web=1&e=vExLV4). 

## Adding a New Tool/Page 
1. Go to the `pages/tools/` folder and create a new JS file for your tool. Add the logic this tools UI.
2. If your tool has parameters that require user input, you can set those up in the left side menu. To do so, follow these steps: 
    1. Go to the `src/components/tools/settings` folder and copy the `settings_template.py` file then rename it with your tool name. 
    2. Address all the `TODO` comment statements in the template and add in your settings logic. 
    3. Within the same folder, go to the `index.js` file and add your new settings component as an export. 
    4. Go to the file `src/layouts/LeftPanel.js` and add your settings component to both the `../components/tools/settings` import and to the `toolSettings` dictionary, add your tool name as the key. 
    5. Go to the file `src/contexts/ToolSettingsContext.js`, create a new React `useState` for the left panel parameter default states. Then add a function to update the React state with new parameter values. Include both in the `value` object at the bottom of the file. 
    6. (Optional) To prevent issues with passing the parameters to the backend, cleaning/processing can be done to ensure compatibility. Go to the file `src/utils/settingsAdapter.js` create a new export function for your tool left panel parameters and add it to the adapters dictionary at the bottom of the file.
3. For any calls/requests made to the tool call one of the functions defined in `services/apiService.js`. 
If you need to add a new API route for the tool: 
    1. Create a new function in `services/apiService.js` that makes this new API request. 
4. Add in the language/translation logic: 
    1. Create a new JS file for your tool in the `translations/tools/` folder.  
    2. In this new file, export 2 dictionaries, one called `en` for all text used in the tool’s UI page and `fr` for all the translated text. Both dictionaries must share the same keys. 
    3. In the same folder, go to the `index.js` file. Import the translation page, then add it to both the export and the `toolMap` dictionary. 
    4. Add in the name of your tool in English and French in the list of tools found in `translations/layout.js` and `translations/components/aiToolsDropdown.js` files. 
    5. In the `utils/translations/toolTranslations.js` file, add a mapping for the new translation page for the tool. The name used should match the filename and will be key used in the UI tool page for accessing its English/French text. 
    6. In the new tool UI file, import `useLanguage` from the contexts folder and `getToolTranslations` from utils. You can then retreive the language dictionaries as so: 
``` javascript
const { language } = useLanguage(); 
const toolData = getToolTranslations("toolName", language);
```
5. Add tool to menu options so users can see the tool by following these steps: 
    1. Go to the `src/page/tools/index.js` file and add your new tool UI page as an export. 
    2. Go to the `src/layouts/Dashboard.js` file, import your tool’s UI page, and add it to the `toolComponents` dictionary. 
    3. Go to the file `src/utils/constants.js` define a new object for your tool, then add your new object to the `TOOL_CATEGORIES` export under the most relevant section (for example if the tool uses OpenAI put it under Large Language Models) 
 
## Current OCDS E-AI Hub Tools 
This section covers all of the tools currently deployed on the OCDS E-AI Hub. <br>
The source code for all the UI pages for all these tools are found in the `./src/pages/tools/` folder except for the AI Inventory Form located in `./src/pages/SurvayForm/` and the Statistical and ML Algorithms Guide UI found in `./src/pages/DocxEditor.js`. 

### Computer Vision 
#### Scale Ageing 
This tool uses a computer vision model trained on annotated salmon scale images to estimate fish age with high accuracy. It automates ageing for fisheries research and management. <br>

The tool originates from a pilot project to help reduce the manual workload currently born by subject matter experts (SMEs) for the DFO Science Branch's Sclerochronology Lab (Fish Ageing Lab). During this pilot, a YOLOv9 model was developed that achieved high accuracy in detecting scale features (clipping, center points, and fragments). The tool also provides transparent explanations by identifying and displaying winter ring patterns corresponding to age determination. <br>

For more detailed documentation specifically on this project, see the [Scale Aging Lessons Learned](https://086gc.sharepoint.com/:w:/r/sites/OCDO/_layouts/15/Doc.aspx?sourcedoc=%7BF61D0A3A-169E-4D70-8C54-A488CAB8BE3E%7D&file=Scale%20Aging%20Lessons%20Learned_EN.docx&action=default&mobileredirect=true). 

The git repo for this tool's API serivce can be found [here](https://github.com/dfo-mpo/scale-age).

#### Fence Counting 
This tool uses computer vision to analyze each frame of river monitoring videos, detecting and classifying salmon as they pass through counting fences. The AI model helps automate species identification and improve accuracy in population tracking. <br>

This tool originates from a pilot project to help DFO’s Science Branch’s Stock Assesment reduce time spent on manually review of underwater footage to count and identify migrating salmon and therefore minimize delays in data availability. <br>

During the pilot, a YOLOv11 detection model was successfully trained and integrated with BOT-SORT tracking algorithms to identify and count five salmon species: Pink, Chum, Chinook, Sockeye, and Coho. The model achieved 87% precision and 88% recall, demonstrating near-expert-level performance. When deployed, this system tracks individual fish throughout video segments and generates automated counts, eliminating the need for frame-by-frame manual review. <br>

For more detailed documentation specifically on this project, see the [Fence Counting Lessons Learned](https://086gc.sharepoint.com/:w:/r/sites/OCDO/_layouts/15/Doc.aspx?sourcedoc=%7BF2769DB9-ACA1-4905-8293-41B2A7AFF4DC%7D&file=Fence%20Counting%20Lessons%20Learned_EN.docx&action=default&mobileredirect=true). 

The git repo for this tool's web interface can be found [here](https://github.com/dfo-mpo/pssi-image-recognition/tree/webInterface).

#### Electronic Monitoring 
This tool is a proof-of-concept demo for DFO's Automated Electronic Monitoring. The project aims to modernize the currently labour-intensive process of manually reviewing video footage of selected sets of tows. The underlying fish counting model was developed in collaboration with the Pacific Groundfish EM Program and various industry partners. The model is capable of identifying and counting in real-time commonly harvested fish species in imagery collected from electronic monitoring equipment onboard commercial fishing vessels. 

The application is hosted on a different web application used by the OCDS team using Gradio. The version on the OCDS E-AI Hub is created by using an iframe rendering the Gradio page. As a result, it has its own English/French toggle that is independent of the AI Hub’s toggle. 

More details about the models used, see [Overview | DFO-MPO](https://ocds-ai-portal.canadacentral.cloudapp.azure.com/details/). 

The git repo for this tool's web interface can be found [here](https://github.com/dfo-mpo/OCDS-AI-Portal).

#### Underwater Marine Life Annotation 
Proof-of-concept demo for DFO Underwater Benthic Marine species identification. This project proposed by Quebec Region's science team aims to automate the review of underwater imagery and video footage collected for biodiversity surveys. The model developed is currently capable of identifying 21 benthic marine life categories drawn from underwater remotely operated vehicles. The project has also since garnered support from the science teams of other regions including Pacific Region. 

The application is hosted on a different web application used by the OCDS team using Gradio. The version on the AI Hub is created by using an iframe rendering the Gradio page. As a result, it has its own English/French toggle that is independent of the AI Hub’s toggle. 

More details about the models used, see [Overview | DFO-MPO](https://ocds-ai-portal.canadacentral.cloudapp.azure.com/details/). 

The git repo for this tool's web interface can be found [here](https://github.com/dfo-mpo/OCDS-AI-Portal).

#### Fish Population Estimation 
This tool is a proof-of-concept demo for an AI-based tool for DFO's underwater fish population estimation tasks. This project explores the potential of a tool that automates detection and estimation of the number of fish in underwater shoals and schools in imagery collected from camera equipment during underwater surveys. The model was developed as a by-product of the EM project, but it has since garnered interest from various programs like the Pacific Salmon Strategy Initiative where we are investigating the potential to leverage this model to automate salmon identification and counting. 

The application is hosted on a different web application used by the OCDS team using Gradio. The version on the OCDS E-AI Hub is created by using an iframe rendering the Gradio page. As a result, it has its own English/French toggle that is independent of the AI Hub’s toggle. 

More details about the models used, see [Overview | DFO-MPO](https://ocds-ai-portal.canadacentral.cloudapp.azure.com/details/). 

The git repo for this tool's web interface can be found [here](https://github.com/dfo-mpo/OCDS-AI-Portal).

#### Detection of Ghost Gear 
Proof-of-concept demo for DFO's Side-scan Sonar Image Ghost Gear Detector. This project was undertaken in partnership with the Ghost Gear Program and aims to automate the process of reviewing side-scan sonar imagery. The system developed leverages an AI-based computer vision model trained on data provided by CSR GeoSurveys Ltd. to identify in real-time Ghost Gear (Abandonned Lobster Traps) from collected side-scan sonar imagery. 

The application is hosted on a different web application used by the OCDS team using Gradio. The version on the AI Hub is created by using an iframe rendering the Gradio page. As a result, it has its own English/French toggle that is independent of the AI Hub’s toggle. 

More details about the models used, see [Overview | DFO-MPO](https://ocds-ai-portal.canadacentral.cloudapp.azure.com/details/). 

The git repo for this tool's web interface can be found [here](https://github.com/dfo-mpo/OCDS-AI-Portal).

#### CTD Data Quality Control 
Proof-of-concept demo for DFO Pacific Region CTD (Conductivity-Temperature-Depth) Data Quality Control model. CTD profiles are depth-wise series' of sensor measures for oceanographic data taken at fixed locations. Challenging ocean conditions and sensor faults can lead to poor quality data that must be manually identified and removed by oceanographers. This project was developed in collaboration with the Pacific Region Ocean Sciences Division and aims to accelerate the CTD quality control process by flagging bad data to assist oceanographers in more rapidly identifying and removing the bad data. Through experimental results, the model achieves 92.6% global accuracy in identifying bad data. The project has also since gained interest from the oceanography teams of other regions including Maritime Region. 

The application is hosted on a different web application used by the OCDS team using Gradio. The version on the OCDS E-AI Hub is created by using an iframe rendering the Gradio page. As a result, it has its own English/French toggle that is independent of the AI Hub’s toggle. 

More details about the models used, see [Overview | DFO-MPO](https://ocds-ai-portal.canadacentral.cloudapp.azure.com/details/). 

The git repo for this tool's web interface can be found [here](https://github.com/dfo-mpo/OCDS-AI-Portal).

#### Classification Model 
This tool sends your image to the already-built Azure Custom Vision models and returns a predicted label + confidence. All models are accessed via the external API service through the OCDS E-AI Hub. 

For more detailed and technical documentation specifically on this tool, see the [Image Classification Model Documentation](https://086gc.sharepoint.com/:w:/r/sites/OCDO/_layouts/15/Doc.aspx?sourcedoc=%7BCC141451-EE6D-4B10-B9CF-DCEE1B1275B3%7D&file=Image%20Classification%20Model%20Documentation.docx&action=default&mobileredirect=true). 

The git repo for this tool's API serivce can be found [here](https://github.com/dfo-mpo/SDPA-AI-Portal/tree/classification).

### Large Language Models 
#### CSV/PDF Analyzer 
This tool enables structured document analysis by processing CSV-based prompts against PDF files. Users can define specific questions or extraction tasks in a CSV file, and the tool will analyze the uploaded document accordingly. 

This tool originates from pilot projects aiming to use OCR and OpenAI to extract and summarize data from documents. A prebuilt OCR extraction model from Azure Document Intelligence is used to process the uploaded document, and then Azure OpenAI is used on the prompts defined in the CSV file to summarize relevant data with source references. Prompt engineering techniques (question formation and structuring) developed throughout the pilot are used on all prompts in the provided CSV file. 

For more detailed documentation specifically on this project, see the [RCOE Lessons Learned](https://086gc.sharepoint.com/:w:/r/sites/OCDO/_layouts/15/Doc.aspx?sourcedoc=%7B802054AF-F14F-47E2-8C5E-9CF22AC3A3F9%7D&file=RCOE%20Lessons%20Learned_EN.docx&action=default&mobileredirect=true). 

The git repo for this tool's API serivce can be found [here](https://github.com/dfo-mpo/openAI-Script/tree/api_service).

#### PDF Chatbot 
This tool uses OpenAI's language model to answer questions about uploaded documents. It provides direct responses with sourced references, making document exploration faster and more efficient. 

Like the CSV/PDF Analyzer, this tool originates from pilot projects using OCR and OpenAI to extract and summarize data from documents; however, it does one prompt at a time and uses retrieval-augmented generation (RAG) using chromadb. RAG allows only relevant chunks of the uploaded document to be passed to OpenAI for a given prompt, reducing processing time and cost. 

For more detailed and technical documentation specifically on this tool, see the [PDF Chatbot Documentation](https://086gc.sharepoint.com/:w:/r/sites/OCDO/_layouts/15/Doc.aspx?sourcedoc=%7BCFB8CB0C-145E-4218-BD70-F0D0A1E9C110%7D&file=PDF%20Chatbot%20Documentation.docx&action=default&mobileredirect=true). 

The git repo for this tool's API serivce can be found [here](https://github.com/dfo-mpo/pdf-chatbot).

#### PII Redactor 
This tool leverages [Microsoft Presidio](https://microsoft.github.io/presidio/) to detect and redact Personally Identifiable Information (PII) such as names, addresses, and phone numbers in PDF documents. It helps enhance data privacy by automatically censoring sensitive content. 

OCR is used to extract the text from the uploaded PDF and after Presidio is used, the uploaded PDF is modified with black boxes placed over all text determined to be sensitive content. This tool works well in some cases but needs to be future explored and developed to have useful applications in DFO. 

For more detailed documentation specifically on this project, see the [Personally Identifiable Information Documentation](https://086gc.sharepoint.com/:w:/r/sites/OCDO/_layouts/15/Doc.aspx?sourcedoc=%7BFDA3415D-7BC8-47F4-B563-56DD5868D169%7D&file=Personally%20Identifiable%20Information.docx&action=default&mobileredirect=true). 

The git repo for this tool's API serivce can be found [here](https://github.com/dfo-mpo/pii-detection).

#### Sensitivity Score Calculator 
This tool uses [Microsoft Presidio](https://microsoft.github.io/presidio/) to analyze documents and determine their sensitivity score based on the presence of Personally Identifiable Information (PII). The higher the score, the more likely a document contains sensitive information. 

OCR is used to extract the text from the uploaded PDF and after Presidio is used, a score is calculated based on the type of sensitive data detected and the number of detections. This tool works well in some cases but needs to be future explored and developed to have useful applications in DFO. 

For more detailed documentation specifically on this project, see the [Personally Identifiable Information Documentation](https://086gc.sharepoint.com/:w:/r/sites/OCDO/_layouts/15/Doc.aspx?sourcedoc=%7BFDA3415D-7BC8-47F4-B563-56DD5868D169%7D&file=Personally%20Identifiable%20Information.docx&action=default&mobileredirect=true). 

The git repo for this tool's API serivce can be found [here](https://github.com/dfo-mpo/pii-detection).

#### French Translation 
This tool uses Google's multilingual AI model ([MADLAD400 10B](https://huggingface.co/google/madlad400-10b-mt)) to translate PDF documents from English to French. It provides fast and efficient translations for various types of content while maintaining context and readability. 

This tool originates from a pilot project aimed to create a LLM that can translate English to French at the level of the French Translation Bureau. Training was done by collecting English-French text pairs from translated documents and fine-tuning an existing LLM with the training data. Although the pilot has been on hold due to lack of training documents and capacity, the latest iteration was proven to provide more accurate translations in a DFO context compared to other publicly available LLM tools. 

For more detailed documentation specifically on this project, see the [French Translation Lessons Learned](https://086gc.sharepoint.com/:w:/r/sites/OCDO/_layouts/15/Doc.aspx?sourcedoc=%7B7AC1D3B1-520F-4305-8FE7-0F1ED2610F5D%7D&file=French%20Translation%20Lessons%20Learned_EN.docx&action=default&mobileredirect=true). 

The git repo for this tool's API serivce can be found [here](https://github.com/dfo-mpo/french-translation-llm/tree/API_tool).

#### Web Scraper 
This tool allows users to input a website URL and automatically scrape its contents for structured data extraction. Once scraped, users can ask questions about the page using OpenAI-powered analysis. Ideal for quick insights, research, or prototyping, this scraper simplifies the process of turning raw web content into actionable answers. 

At a high level, the solution works in two ways: 
1. Scrape once, reuse many times <br>
A user pastes in a public website or intranet URL they care about. The tool automatically visits that site and its key subpages, scrapes the HTML content and reads commonly attached files and splits that content into smaller chunks. Each chunk is converted into an embedding and stored, along with its metadata, in a vector database. This makes the content searchable and reusable. Once a site has been processed, it appears as a “preset card” in the left-hand panel of the Web Scraper page, showing basic details like the site name and last scraped time. 

2. Chat instead of text-hunting <br>
Once a site has been scraped, anyone with access to the AI Portal can select its preset and start chatting with it. Users can ask questions, and the chatbot responds based only on the text that was collected from that site. Behind the scenes, the chatbot looks up the most relevant chunks from the vector database for that site and uses them to generate an answer based only on the prompt. The chat history and the scraped content for each site can be downloaded as simple text files, making it easy to keep a record of what was asked, answered, and scraped. 

From a user’s perspective, this turns a complex website into a single, interactive experience. Over time, a set of commonly used websites can be scraped once and reused by many scientists, analysts, and teams. 

For more detailed and technical documentation specifically on this tool, see the [WebScraper Chatbot Documentation](https://086gc.sharepoint.com/:w:/r/sites/PacificSalmonTeam/_layouts/15/Doc.aspx?sourcedoc=%7B43E161EB-4D11-4214-B6CD-E72F0272B56E%7D&file=WebScraper%20Chatbot%20Documentation.docx). 

The git repo for this tool's API serivce can be found [here](https://github.com/dfo-mpo/web-scraper)

### Optical Character Recognition 
#### Document OCR 
This tool allows users to upload a PDF and automatically scrape its contents for structured data extraction. Once scraped, users can ask questions about the PDF using OpenAI-powered analysis. Ideal for quick insights, research, or prototyping, this tool simplifies the process of turning raw PDF content into actionable answers. 

For more detailed and technical documentation specifically on this tool, see the [PDF Extraction Tool Documentation](https://086gc.sharepoint.com/:w:/r/sites/OCDO/_layouts/15/Doc.aspx?sourcedoc=%7B60BDA078-BC15-4784-836E-03F2FF21C758%7D&file=PDF%20Extraction%20Tool%20Documentation.docx&action=default&mobileredirect=true). 

The git repo for this tool's API serivce can be found [here](https://github.com/dfo-mpo/ocr-document-intelligence/tree/openai-ocr).

#### OCR Review Tool
This tool allows users to review documents that have been processed using Azure Document Intelligence's OCR custom models. The tool hosted in the OCDS E-AI Hub is a demo version with several unprotected documents that have been copied from real proof-of-concept projects. <br>
The interface allows users to quickly identify what has been detected by the OCR model and make any corrections. It supports adding a status to each document, such as if it has been reviewed or if it has a problem. 

For more detailed documentation specifically on this project, see the [FFHPP Lessons Learned](https://086gc.sharepoint.com/:w:/r/sites/OCDO/_layouts/15/Doc.aspx?sourcedoc=%7BAE91C791-6872-4038-9194-735D3E144A63%7D&file=FFHPP%20Lessons%20Learned_EN.docx&action=default&mobileredirect=true), [QCFM Lessons Learned](https://086gc.sharepoint.com/:w:/r/sites/OCDO/_layouts/15/Doc.aspx?sourcedoc=%7B7E1FE8AE-9279-4458-908A-AFFA55C45576%7D&file=QCFM%20Lessons%20Learned_EN.docx&action=default&mobileredirect=true), or [FM Lessons Learned](https://086gc.sharepoint.com/:w:/r/sites/OCDO/_layouts/15/Doc.aspx?sourcedoc=%7B211B9679-46DC-4928-9AF9-A0714869AB72%7D&file=FM%20Lessons%20Learned_EN.docx&action=default&mobileredirect=true). 

The git repo for this tool's web interface can be found [here](https://github.com/dfo-mpo/ocr-json2web).

### Model Repo 
#### Models 
A unified repository where users can upload, explore, and manage machine learning models. It supports versioning and model cards with key metadata to help teams quickly integrate models into their workflows. Users can browse existing models from OCDS and SDPA or contribute their own. 

The solution introduces a model repository within the OCDS E-AI Hub, designed specifically to showcase the models that scientists have already built and trained. Rather than performing any machine learning tasks itself, the repository acts as a window into what already exists in Azure Machine Learning workspace which includes model versions, metadata, READMEs, tags, and artifacts stored within the MLflow registry server and Blob Storage.  

Users continue to upload, version, and manage their models entirely through the AML workspace, while the repository simply exposes this information through the OCDS E-AI Hub. The backends' endpoints communicate directly with AML to retrieve lists of models, fetch metadata, download artifacts, and extract READMEs. The frontend then presents this information in a consistent, searchable, and user-friendly catalogue. The result is a centralized hub that makes internal models easy to discover and reuse while keeping all model lifecycle operations inside AML. 

For more detailed and technical documentation specifically on this tool, see the [ML Model Repo Documentation](https://086gc.sharepoint.com/:w:/r/sites/PacificSalmonTeam/_layouts/15/Doc.aspx?sourcedoc=%7B9e61821f-450d-4817-b33c-f468ed18f0f1%7D). 

The git repo for this tool's web interface can be found [here](https://github.com/dfo-mpo/SDPA-AI-Portal/tree/ml-models-repo).

### AI Inventory Form 
#### Form 
This form is meant to be use as guide to support business users in articulating and imagining the potential of using Data, Artificial Intelligence, and Machine Learning to improve productivity, efficiencies, and generate value for program and service delivery, operations, and other business processes. It is meant to help users determine the value and potential of new data innovation from a value proposition, scalability, and sustainability lens rather than a technical implementation perspective. Complete responses will help Data and AI Scientist to determine how feasible a solution could be. 

For more information on mapping AI intitiatives, advancing AI use cases, and analyzing AI initiatives, see the [AI Enablement Site](https://086gc.sharepoint.com/sites/AIEnablementActivationdelIA/SitePages/ProjectHome.aspx?csf=1&web=1&e=IVjjIm&CID=7229b7a1-b01e-9000-c80d-b5d30c2f75a9&cidOR=SPO&OR=Teams-HL&CT=1767809285809&isSPOFile=1&xsdata=MDV8MDJ8fDRmZjVjMTk4NDYyNTQ1ZjgzY2FiMDhkZWJiNGU0YmY2fDE1OTRmZGFlYTFkOTQ0MDU5MTVkMDExNDY3MjM0MzM4fDB8MHw2MzkxNTQxNDIwODk0NjA5MDd8VW5rbm93bnxWR1ZoYlhOVFpXTjFjbWwwZVZObGNuWnBZMlY4ZXlKRFFTSTZJbFJsWVcxelgwRlVVRk5sY25acFkyVmZVMUJQVEU5R0lpd2lWaUk2SWpBdU1DNHdNREF3SWl3aVVDSTZJbGRwYmpNeUlpd2lRVTRpT2lKUGRHaGxjaUlzSWxkVUlqb3hNWDA9fDF8TDJOb1lYUnpMekU1T20xbFpYUnBibWRmV1RKUk1WcFVWVEphYWtGMFRtMU5NRTU1TURCYVZGSm9URlJvYWsxdFdYUk9WR2Q1VG5wSmVVNHlUWGxOUkdSclFIUm9jbVZoWkM1Mk1pOXRaWE56WVdkbGN5OHhOemM1T0RFM05EQTJOVEV4fGRkOWRkYmI1ZTM2NzQxNjEzY2FiMDhkZWJiNGU0YmY2fGY5Yjk3YTkwNmYwYzQzZDQ4N2Q0MzVjMGU5ODUxMmFm&sdata=alpod3pKeFppRVU0TUE4VGJ0bHd5MUppUXd5eFM3Q2tESFA2bHphOFdQWT0%3D&ovuser=1594fdae-a1d9-4405-915d-011467234338%2CDavid.Onak%40dfo-mpo.gc.ca&TeamsCID=0511a010-24f1-4d41-a9ee-109c9a87e5a5&clickparams=eyJBcHBOYW1lIjoiVGVhbXMtRGVza3RvcCIsIkFwcFZlcnNpb24iOiI0OS8yNjA0MzAxOTIxNiJ9&linkOpenTime=1779835334937#welcome-to-the-ai-enablement-site).

### Statistical and ML Algorithms Guide 
#### Document 
This document will describe different categories of machine learning algorithms and their intended purposes, specifically supervised learning followed by unsupervised learning. Individual algorithms will be explained, and a template will be provided for each algorithm that can be used out-of-box. 

This document is strictly scoped to the selection and training of ML models, which are a subset of tasks within the broader domains of ML Ops and AI Governance. There are many other tasks and responsibilities that constitute effective and responsible development, deployment and usage of ML models. The breadth of information needed to fully cover these domains requires a suite of policy, guidance, and educational materials. This document can be seen as one component of this broader suite that is currently being assembled within DFO. 

See the [Statistical and ML algorithms Guide](https://086gc.sharepoint.com/:w:/r/sites/DataEthicsWorkingGroup/_layouts/15/Doc.aspx?sourcedoc=%7BEF8A436D-7BA0-422E-89D9-211130F5C7EB%7D&file=Statistical%20and%20ML%20algorithms%20Guide.docx&action=default&mobileredirect=true).
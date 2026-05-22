# ML Models Repo Tool
A unified repository where users can upload, explore, and manage machine learning models. It supports versioning and model cards with key metadata to help teams quickly integrate models into their workflows. Users can browse existing models from OCDS and SDPA or contribute their own. 

The solution introduces a model repository within the AI Hub, designed specifically to showcase the models that scientists have already built and trained. Rather than performing any machine learning tasks itself, the repository acts as a window into what already exists in Azure Machine Learning workspace which includes model versions, metadata, READMEs, tags, and artifacts stored within the MLflow registry server and Blob Storage.  

Users continue to upload, version, and manage their models entirely through the AML workspace, while the repository simply exposes this information through the AI Hub. The backends' endpoints communicate directly with AML to retrieve lists of models, fetch metadata, download artifacts, and extract READMEs. The frontend then presents this information in a consistent, searchable, and user-friendly catalogue. The result is a centralized hub that makes internal models easy to discover and reuse while keeping all model lifecycle operations inside AML. 

For more detailed and technical documentation specifically on this tool, see the [ML Model Repo Documentation](https://086gc.sharepoint.com/:w:/r/sites/OCDO/Shared%20Documents/07%20-%20Data%20Science/26%20-%20PSSI-SDPA/10%20-%20Documentation/01%20-%20Data%20Analytics%20Team/17%20-%20DFO%20AI%20Hub/01%20-%20ML%20Model%20Repo/ML%20Model%20Repo%20Documentation.docx?d=w74f621f7c9c04f4bb05fb64c24720471&csf=1&web=1&e=TuEdLe). 

This interface is meant to be embedded as an iframe on the OCDS Educational AI Hub found [here](https://github.com/dfo-mpo/SDPA-AI-Portal).

## Framework/structure
### Backend/API
The backend component is a [Unvicorn](https://uvicorn.dev/) project (which is running FastAPI and Python v3.10) located under `./api/`. This component handles all API requests from the React frontend. 

It is recommended to use a virtual environment which has its route path defined in the `.gitingore` and `./api/.dockerignore` files to prevent unnecessary copying of the virtual environment.  

All dependencies used in this component are defined in the `/api/requirements.txt` file, and it is important to use Python v3.10 as other python versions will likely fail when installing the libraries. 

### Frontend
The frontend component is a [React](https://react.dev/) (version 18.3.1) with material UI (version 6.4.7) for many UI components. The code for this component can be found in the `./src` folder with index.js being the startup file/entry point. It uses nginx when hosted as docker containers to reroute API requests internally to the backend. This is defined in `nginx-app.conf`.

The frontend is structured as so:
- `components` - files containing smaller, reusable components.
- `context` - files used to manage global states (i.e. current language).
- `layout` - larger components that define the structure/layout.
- `pages` - JS files that build each of the pages used in the AI Hub.
- `pages/services` - logic for all requests made to the backend.
- `styles` - files containing CSS styling or overrides for material UI components.
- `translations` - files defining objects containing all English-French pairs for the AI Hub so it can support both languages.
- `utils` - helper and miscellaneous files used in the frontend.

All dependencies used in this component are defined in the `package.json` and `package-lock.json` files.

## HTTP Requests Handled Internally   
Requests are handled in the `/api/main.py` file. The API exposes the following endpoints:  
  
- **`GET /models`**    
  Returns the latest version of each registered model in the Azure ML workspace.  
  
  Query parameters:  
  - `force` (optional): If `true`, bypasses the in‑memory cache and fetches fresh data from Azure ML  
  
  Behavior:  
  - Lazily initializes the Azure ML client  
  - Uses a short‑lived in‑memory cache (5 minutes) to reduce API calls  
  - Returns only the most recent version per model, sorted by last update time  
  
  Each model entry includes:  
  - Name and version  
  - Description, type, and flavors  
  - Tags  
  - Creation and last‑updated timestamps  
  
- **`GET /models/{name}/versions`**    
  Returns all versions for a given model.  
  
  Behavior:  
  - Fetches all registered versions from Azure ML  
  - Sorts versions in descending order (newest first)  
  
  Each entry includes the same metadata fields as the `/models` endpoint.  
  
- **`GET /models/{name}/versions/{version}/download.zip`**    
  Downloads all artifacts for a specific model version as a ZIP file.  
  
  Behavior:  
  - Downloads the model artifacts to a temporary directory via Azure ML  
  - Packages the directory into a ZIP archive  
  - Streams the ZIP file to the client  
  - Automatically cleans up temporary files after the response completes  
  
- **`GET /models/{name}/versions/{version}/readme`**    
  Returns the README file for a specific model version, if present.  
  
  Query parameters:  
  - `force` (optional): If `true`, bypasses the README cache and re‑downloads artifacts  
  
  Behavior:  
  - Searches downloaded model artifacts for files named `README*`  
  - Supports Markdown and plain‑text README formats  
  - Uses a per‑model/version in‑memory cache (5 minutes)  
  - Returns `404` if no README is found  
  
  Response shape:  
  - `filename`: Name of the README file  
  - `media_type`: MIME type (`text/markdown` or `text/plain`)  
  - `content`: Raw README contents  
  
#### Error Handling and Configuration  
- Returns **`503 Service Unavailable`** if the Azure ML workspace is not configured  
- Requires the following environment variables:  
  - `AZURE_SUBSCRIPTION_ID`  
  - `AZURE_RESOURCE_GROUP`  
  - `AZURE_ML_WORKSPACE`  
  
All endpoints support CORS and are designed to be consumed by the associated frontend applications. 

## Intial Setup
Before this API can be run, the chroma database and enviroment variables need to be intialized.
1. Create a new file in `/api` called `.env` by copying `api/.env.example` and filling in the missing keys for the required Azure resources. Instead of adding in the keys to the `.env` file you can add a `KEY_VAULT_NAME` for a key vault containing the keys either in the `.env`, the `docker-compose.yml`, or in the resource running the docker instance. Note that if you are using a key vault for API secrets, it will only work when hosted on Azure resources with access to the key vault.

## Run Web Interface
You can run the API by running the `docker-compose.yml` file which creates a container for the React frontend and FastAPI backend. Use the following command:
```bash
docker-compose up --build
```
Note that this will fail to connect to the 

## Update Deployment
This tool is currently hosted in the OCDS SSC (Shared Services Canada) Azure environment to be used by the OCDS Educational AI Hub. To update the deployment follow the steps below:
1. Run the command `docker-compose up --build` to update your local docker instance with the latest changes.
2. Update the docker images used hosted in the SSC Azure environment by running the following commands in a terminal (note you will need to download [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-windows?view=azure-cli-latest&pivots=msi) if you don't have it):
```bash
az login --tenant 8c1a4d93-d828-4d0e-9303-fd3bd611c822
az acr login --name sdpatools
docker tag ml-models-repo-backend sdpatools.azurecr.io/portal-tools/ml-models-repo-backend:latest
docker tag ml-models-repo-frontend sdpatools.azurecr.io/portal-tools/ml-models-repo-frontend:latest
docker push sdpatools.azurecr.io/portal-tools/ml-models-repo-backend:latest
docker push sdpatools.azurecr.io/portal-tools/ml-models-repo-frontend:latest
```
3. Lastly, you will need to restart the [web application](https://portal.azure.com/#@163oxygen.onmicrosoft.com/resource/subscriptions/4858d1be-583d-42d6-a4a3-44172168b003/resourceGroups/Merged-AI-Portal-Frontend-RG/providers/Microsoft.Web/sites/ml-model-repo-demo/appServices) to ensure the latest version of the images are pulled. If a different tag is used (instead of :latest) you will need to update the tag from the images to use instead.
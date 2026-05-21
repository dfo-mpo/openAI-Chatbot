# Classification Model Tool API
This tool sends your image to the already-built Azure Custom Vision models and returns a predicted label + confidence. All models are accessed via the HTTP requests using the `httpx` library. 

Detailed documenation on this tool can be found [here](https://086gc.sharepoint.com/:w:/r/sites/OCDO/_layouts/15/Doc.aspx?sourcedoc=%7BCC141451-EE6D-4B10-B9CF-DCEE1B1275B3%7D&file=Image%20Classification%20Model%20Documentation.docx&action=default&mobileredirect=true).

Note that this repository is strictly the backend logic for this tool. The frontend is hosted on the OCDS Educational AI Hub found [here](https://github.com/dfo-mpo/SDPA-AI-Portal).

## HTTP Requests Handled Internally  
  
Requests are handled in the `app/main.py` file. The API exposes the following endpoints:  
  
- **`GET /classificationmodels`**    
  Returns a list of available and properly configured classification models.    
  Each model entry includes:  
  - `id`: Internal model identifier  
  - `name`: Human‑readable model name  
  - `description`: Short description of the classifier    
  Only models with valid prediction URLs and keys configured via environment variables / Azure Key Vault are returned.  
  
- **`POST /predict/{model_id}`**    
  Runs an image classification prediction using the specified model.    
  - `model_id` (path parameter): Identifier of the classification model (e.g., `fresh-vs-infected-salmon`)    
  - Accepts an uploaded image file (`jpg`, `jpeg`, `png`, `bmp`, `webp`, max 8 MB)  
  
  Processing steps:  
  - Validates the model configuration  
  - Validates file type and size  
  - Forwards the image bytes to the corresponding Azure Custom Vision prediction endpoint  
  - Parses and sorts prediction results by confidence  
  
  The response includes:  
  - `label`: Top predicted class label  
  - `confidence`: Probability score of the top prediction  
  - `predictions`: List of all predicted labels with confidence scores  
  
All endpoints support CORS and are designed to be consumed by the associated frontend applications.  

## Intial Setup
Before this API can be run, the enviroment variables need to be intialized.
1. Create a new file in `/app` called `.env` by copying `app/.env.example` and filling in the missing keys for the required Azure resources. Instead of adding in the keys to the `.env` file you can add a `KEY_VAULT_NAME` for a key vault containing the keys either in the `.env`, the `docker-compose.yml`, or in the resource running the docker instance. Note that if you are using a key vault for API secrets, it will only work when hosted on Azure resources with access to the key vault.

## Run API
You can run the API by building the docker image then running a container for it. Use the following commands:
```bash
docker build -t classification:latest .
docker run -d -p 8080:8000 --name classification classification
```
This will create an image called `classification` then run it in a container called `classification` hosted on port `8080`.

## Update Deployment
This tool is currently hosted in the OCDS SSC (Shared Services Canada) Azure environment to be used by the OCDS Educational AI Hub. To upload the deployment follow the steps below:
1. Run the command `docker build -t classification:latest .` to update your local docker instance with the latest changes.
2. Update the docker image used hosted in the SSC Azure environment by running the following commands in a terminal (note you will need to download [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-windows?view=azure-cli-latest&pivots=msi) if you don't have it):
```bash
az login --tenant 8c1a4d93-d828-4d0e-9303-fd3bd611c822
az acr login --name AIPortal
docker tag classification aiportal.azurecr.io/ocds-ai-portal/pssi-classification:latest
docker push aiportal.azurecr.io/ocds-ai-portal/pssi-classification:latest
```
3. Lastly, you will need to SSH into the [VM](https://portal.azure.com/#@163oxygen.onmicrosoft.com/resource/subscriptions/4858d1be-583d-42d6-a4a3-44172168b003/resourceGroups/ocds-ai-portal/providers/Microsoft.Compute/virtualMachines/OCDS-AI-Portal-VM/overview) hosting the API and rerun its `docker-compose.yml` to use the latest version of the docker image.
# DFO OCDS E-AI Hub
This repository is for the DFO Office of the Chief Data Steward (OCDS) Educational AI Hub (OCDS E-AI Hub), a platform designed to explore the potential of artificial intelligence in fisheries and oceans research. Our initiatives harness the power of advanced data and A.I. technologies like machine learning, computer vision, and natural language processing to revolutionize how to support marine conservation and rebuilding efforts in the modern data and digital era.

These tools are prototypes designed to illustrate possible AI applications for DFO scientists, therefore, are strictly for educational purposes and are not to be used in any work processes. Please avoid uploading any sensitive or operational data if using this tool.

If you plan on contributing to new features, imporving the OCDS E-AI Hub, or updating Azure hosted instance check out the [CONTRIBUTE](CONTRIBUTE.md) page.

## Code Overview
The OCDS E-AI Hub is responsible for the interface users interact with and the authentication of users. It uses an iframe or API service for each tool hosted.

The OCDS E-AI Hub is implemented using React JS (version 18.3.1) with material UI (version 6.4.7) for many UI components. The code for this component can be found in the `./src` folder with `index.js` being the startup file/entry point. The frontend is structured as so:
- components - files containing smaller, reusable components, including logic for authenticating users to the portal.
- context - files used to manage global states (i.e. user authenticated, or current language).
- hooks - contains reusable logic such as handling file upload for a button.
- layout - larger components that define the structure/layout of the OCDS E-AI Hub UI.
- pages - JS files that build each of the pages used in the OCDS E-AI Hub.
- services - logic for all requests made to the backend.
- styles - files containing CSS styling or overrides for material UI components.
- translations - files defining objects containing all English-French pairs for the OCDS E-AI Hub so it can support both languages.
- utils - helper and miscellaneous files used in the frontend.

See [FRONTEND](src/FRONTEND.md) for more details on this component. 

## Building the Docker Container Locally
To run this locally, open a terminal an run the command `npm run dev`. <br>
The docker-compose.yml file will allow for a docker container be created using the frontend, chroma, and backend images. It reroutes the frontend exposure port to 3080.
### Prerequisites (if you don't already have docker)
1. First you need to install the Linux subsystem for Windows, open a PowerShell or Command Prompt terminal using Admin Privileges and run the following command: 
```bash
wsl --install 
```
You may need to restart the computer after this step.

2. Ensure you have docker installed on your device, see link to [downloading docker](https://docs.docker.com/desktop/setup/install/windows-install/).
### Steps to run container locally
To set up your container locally:
1. In the `./src/components/auth/` folder, copy and rename the 'authConfig.example.js' into 'authConfig.js'. Make sure to add in the values for clientId, authority, redirectURI, and postLogoutRedirectUri.
2. Build the local docker container using the command:
```bash
# Use this command if your docker engine version is below 20.10
docker-compose up --build

# Use this command if you have docker engine v20.10 or newer
docker compose up --build
```
You can now use the web app locally from, http://localhost:3080

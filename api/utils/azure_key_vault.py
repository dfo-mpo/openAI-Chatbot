import os
from dotenv import load_dotenv

load_dotenv()
using_AKV = True if os.environ.get("KEY_VAULT_NAME") else False

# make request to AKV for key or get cached secret for CUSTOM_VISION_PREDICTION_KEY (shared key for all models)
def get_CUSTOM_VISION_PREDICTION_KEY():
    if using_AKV: # key vault name is only defined in web app not local .env files
        from core.secrets import get_secret # want managed identity to be ready before loading import, (so we don't import until running the function)
        return get_secret("cv-prediction-key") # AKV does not allow caps and underscores in secret names
    else:
        return os.getenv("CUSTOM_VISION_PREDICTION_KEY")
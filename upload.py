# Set your Cloudinary credentials
# ==============================
from dotenv import load_dotenv
load_dotenv()

# Import the Cloudinary libraries
# ==============================
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Import to format the JSON responses
# ==============================
import json

# Set configuration parameter: return "https" URLs by setting secure=true  
# ==============================
config = cloudinary.config(secure=True)

# Log the configuration
# ==============================
print("****1. Set up and configure the SDK:****\nCredentials: ", config.cloud_name, config.api_key, "\n")
def uploadImage(text, text_id):

  # Upload the image and get its URL
  # ==============================

  # Upload the image.
  # Set the asset's public ID and allow overwriting the asset with new versions
  cloudinary.uploader.upload(text, public_id= text_id,resource_type = "auto", unique_filename = False, overwrite=True)
  print("Upload to the cloud successfully")


  return
  
def fileUrl(text, text_id):
    # Build the URL for the image and save it in the variable 'srcURL'
  srcURL = cloudinary.CloudinaryImage(text_id).build_url()

  # Log the image URL to the console. 
  # Copy this URL in a browser tab to generate the image on the fly.
  print("****Delivery URL: ", srcURL, "\n")
  return
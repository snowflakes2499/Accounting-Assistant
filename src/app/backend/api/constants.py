from django.conf import settings
import os
# Invoice Ninja API settings
INVOICE_NINJA_API_URL = settings.INVOICE_NINJA_API_URL
INVOICE_NINJA_API_TOKEN = settings.INVOICE_NINJA_API_TOKEN
MEDIA_ROOT = settings.MEDIA_ROOT

# Paths: 
WHISPER_CPP_EXECUTABLE = '/home/suyash/whisper.cpp/build/bin/whisper-cli'  
# MODEL_PATH = '/home/suyash/whisper.cpp/models/ggml-base.en.bin'  
MODEL_PATH = '/home/suyash/whisper.cpp/models/ggml-base.bin'  
TRANSCRIBE_OUTPUT_PATH = os.path.join(settings.MEDIA_ROOT, "output.txt")
FFMPEG_EXECUTABLE = 'ffmpeg'  

# Models :

TAB_MODEL_PATH = '/home/suyash/accounting-assistant/src/app/backend/api/pickles/fast_invoice_ninja_tab_classifier.pkl'

# Prompt Templates :
curr_dir = os.path.dirname(os.path.realpath(__file__))
PRODUCT_TEMPLATE_PATH = f'{curr_dir}/templates/Product.txt'
CLIENT_TEMPLATE_PATH = f'{curr_dir}/templates/Client.txt'
INVOICE_TEMPLATE_PATH = f'{curr_dir}/templates/Invoice.txt'
VENDOR_TEMPLATE_PATH = f'{curr_dir}/templates/Vendor.txt'
FEATURE_EXTRACTION_LOC = f'{curr_dir}/templates/FeatureExtract.txt'
REPORT_TEMPLATE_PATH = f'{curr_dir}/templates/Report.txt'
print(f"Product template path: {PRODUCT_TEMPLATE_PATH}")
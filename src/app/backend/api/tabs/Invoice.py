from django.conf import settings
from django.http import JsonResponse

INVOICE_NINJA_API_URL = settings.INVOICE_NINJA_API_URL
INVOICE_NINJA_API_TOKEN = settings.INVOICE_NINJA_API_TOKEN
MEDIA_ROOT = settings.MEDIA_ROOT


class Invoice: 
    
    def appropriate_function(self, transcript):
        
        # use the second NLP model to get the appropriate function
        # pass the transcript to the model
        # get the function name
        # call the function 

        print("Invoice appropriate function called")

        return JsonResponse({"status": "Invoice appropriate function called"})

    
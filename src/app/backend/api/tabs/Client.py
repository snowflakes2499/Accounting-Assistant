from django.conf import settings
from django.http import JsonResponse
import requests
import json
from api.constants import CLIENT_TEMPLATE_PATH
INVOICE_NINJA_API_URL = settings.INVOICE_NINJA_API_URL
INVOICE_NINJA_API_TOKEN = settings.INVOICE_NINJA_API_TOKEN
MEDIA_ROOT = settings.MEDIA_ROOT


class Client: 
    
    def appropriate_function(self, transcript):
        with open(CLIENT_TEMPLATE_PATH) as f:
            prompt = f.read()

        prompt += f""" Now extract from: '{transcript}' """

        OLLAMA_URL = "http://localhost:11434/api/generate"

        data = {
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }

        response = requests.post(OLLAMA_URL, json=data)
        if response.status_code == 200:
            response_string = response.json().get("response", "").strip()
            output_texts = json.loads(response_string)
            print("Output: ", output_texts)

            for output_text in output_texts:
                json_output = output_text
                if "data" in json_output:
                    # operation = json_output.get("operation", "").strip().lower()
                    data = json_output.get("data", {})

                    print("\nThe loan data  ", data)
                    print(f"type of load data {type(data)}")
                    person_name = data.get('personName', '')
                    print(f"person is {person_name}")
                    loanType = data.get('loanType', '')
                    debt_amt = int(data.get('loanAmount', 0))
                    description = data.get('description', '')
                    if "email" in transcript.lower():
                        print("inside the email part")
                        import yagmail
                        yag = yagmail.SMTP("suyashd999@gmail.com", "vhcrdnxvjfoybtyt")
                        response = requests.post(
                            'http://localhost:8080/api/db/loans/loan',
                            json={"personName": person_name.lower()}
                        )
                        print(f"Response fetching email {response}")
                        if response.status_code == 200:
                            response_data = response.json()
                            current_amt = int(response_data.get("loanAmount", 0))
                            existing_desc = response_data.get("description", "")
                            email = response_data.get("email", "")                                
                            print(f"Email sending to is: {email}")
                            yag.send(
                            to=f"{email}",
                            subject=f"Reminder for repayment of ₹{current_amt} ",
                            contents=f"Hi {person_name}! Please pay the due amount."
                            )
                        return JsonResponse({"message": f"Sent email to {email}."}, status=200)
                    # Handle new loan creation
                    if "create new loan" in transcript.lower():
                        print("Creating a brand new loan entry")                        
                        data2 = {
                            "model": "mistral",
                            "prompt": f"""
                        extract the email from the transcript: {transcript}
                        return valid JSON only with this format:
                        {{
                        "email": "example@email.com"
                        }}
                        Do not add any explanation, just the JSON.
                        """,
                            "stream": False
                        }

                        response = requests.post(OLLAMA_URL, json=data2)

                        try:
                            # Get the model's JSON-formatted response
                            response_string = response.json().get("response", "").strip()
                            print("Model response:", response_string)

                            # Parse it
                            extracted_email = json.loads(response_string).get("email", "suyash.dongre23@vit.edu")
                            print("Extracted email:", extracted_email)

                        except Exception as e:
                            print("Error parsing email:", e)
                            extracted_email = "suyash.dongre23@vit.edu"

                        create_res = requests.post(
                            'http://localhost:8080/api/db/loans/create',
                            json={
                                "personName": person_name,
                                "loanAmount": debt_amt,
                                "email": email
                            }
                        )

                        trans_res = requests.post(
                            'http://localhost:8080/api/db/transactions/create',
                            json={
                                "personName": person_name,
                                "loanType": loanType,
                                "loanAmount": debt_amt,
                                "description": description
                            }
                        )

                        if create_res.status_code == 200 and trans_res.status_code == 200:
                            return JsonResponse({"message": f"New loan created for {person_name}."}, status=200)
                        else:
                            return JsonResponse({"error": "Failed to create loan or transaction."}, status=500)

                    # Existing loan update logic
                    response = requests.post(
                        'http://localhost:8080/api/db/loans/loan',
                        json={"personName": person_name}
                    )
                    print("1st RESPONSE ", response.json())

                    if response.status_code == 200:
                        response_data = response.json()
                        current_amt = int(response_data.get("loanAmount", 0))
                        existing_desc = response_data.get("description", "")

                        if loanType == "lent":
                            updated_amt = current_amt + debt_amt
                        elif loanType in ["debt", "repayment"]:
                            updated_amt = current_amt - debt_amt
                        else:
                            continue  # Skip invalid loan types

                        combined_description = f"{existing_desc} {description}".strip()

                        trans_res = requests.post(
                            'http://localhost:8080/api/db/transactions/create',
                            json={
                                "personName": person_name,
                                "loanType": loanType,
                                "loanAmount": debt_amt,
                                "description": description
                            }
                        )

                        update_res = requests.post(
                            'http://localhost:8080/api/db/loans/update',
                            json={
                                "personName": person_name,
                                "loanAmount": updated_amt,
                                "description": combined_description
                            }
                        )

                        if trans_res.status_code == 200 and update_res.status_code == 200:
                            requests.post('http://localhost:8080/api/db/operation',json={
                            "operation":"processing",
                            "status": "false"
                            })
                            return JsonResponse({"message": f"Loan {loanType} recorded successfully."}, status=200)

                    return JsonResponse({"error": f"{person_name} is not in the database!"}, status=404)

                else:
                    print("Invalid JSON structure: 'operation' or 'data' not found")
        else:
            print(f"API request failed with status code: {response.status_code}")

        return JsonResponse({"status": "Client appropriate function called"})

   
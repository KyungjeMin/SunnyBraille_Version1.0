import requests
import json
from django.shortcuts import render
from .models import UploadedFile  # Import your UploadedFile model

APP_ID = 'wpwn1311_yonsei_ac_kr_7c94c3_0a52f4'
APP_KEY = 'fc80bda94239ac26a8df40fd61c758d4956c211f390d053c1c8fc4873eb27063'


def upload_pdf(request):
    if request.method == 'POST' and request.FILES['pdf_file']:
        pdf_file = request.FILES['pdf_file']
        uploaded_file = UploadedFile.objects.create(file=pdf_file)

        # MathPix API 호출
        api_url = "https://api.mathpix.com/v3/pdf"
        headers = {
            "app_id": APP_ID,
            "app_key": APP_KEY
        }
        options = {
            "conversion_formats": {"docx": True, "tex.zip": True},
            "math_inline_delimiters": ["$", "$"],
            "rm_spaces": True
        }
        data = {
            "options_json": json.dumps(options)
        }

        with pdf_file.open(mode = 'rb') as f:
            files = {
                'file' : f
            }
        # API 호출 및 응답 처리
            response = requests.post(api_url, headers=headers, data=data, files=files)

        if response.status_code == 200:
            api_response = response.json()
            pdf_id = api_response.get("pdf_id")
            if pdf_id:
                # 여기에서 pdf_id를 사용하여 원하는 작업을 수행할 수 있습니다.
                # 예를 들어, pdf_id를 사용자에게 보여주거나 다른 API로 전송할 수 있습니다.
                return render(request, 'result.html', {'pdf_id': pdf_id})
            else:
                print("PDF ID not found in API response.")
        else:
            print(f"API request failed with status code: {response.status_code}")
            print(response.text)

    return render(request, 'upload.html')
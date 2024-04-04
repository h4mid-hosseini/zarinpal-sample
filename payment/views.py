import json
from django.conf import settings
import requests
from django.http import JsonResponse
from django.shortcuts import redirect



amount = 25000  # Rial / Required
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
phone = '09121234567'  # Optional
CallbackURL = f'http://127.0.0.1:8000/payment/verify/' 

ZP_API_REQUEST = f"https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://sandbox.zarinpal.com/pg/StartPay/"
MERCHANT = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"



def send_request(request):    
    data = {
        "MerchantID": MERCHANT,
        "Amount": amount,
        "Description": description,
        "Phone": phone,
        "CallbackURL": CallbackURL,
    }

    data = json.dumps(data)
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    try:
        response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)

        if response.status_code == 200:
            json_response = response.json()
            if json_response['Status'] == 100:
                redirect_url = ZP_API_STARTPAY + str(json_response['Authority'])
                return redirect(redirect_url)
            else:
                return JsonResponse({'status': False, 'code': str(json_response['Status'])})
        return JsonResponse(response)
    
    except requests.exceptions.Timeout:
        return JsonResponse({'status': False, 'code': 'timeout'})
    except requests.exceptions.ConnectionError:
        return JsonResponse({'status': False, 'code': 'connection error'})
    






def verify(request):
    query_params = request.GET.copy()
    authority_value = query_params.get('Authority', '')

    data = {
        "MerchantID": MERCHANT,
        "Amount": amount,
        "Authority": authority_value,
    }
    data = json.dumps(data)
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    response = requests.post(ZP_API_VERIFY, data=data, headers=headers)

    if response.status_code == 200:
        response_json = response.json()
        if response_json['Status'] == 100:
            return JsonResponse({'status':'success-payment'})
        else:
            return JsonResponse({'status':'failed-payment'})
    return JsonResponse(response.json())

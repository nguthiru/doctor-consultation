from django.http import HttpResponse,JsonResponse
import requests
from requests.auth import HTTPBasicAuth
import json
from rest_framework.response import Response
from rest_framework.decorators import api_view
import base64
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
class MpesaCredentials:
    consumer_key = 'RT4PNvGMcJqUUUYnObnnDuX5y3AqJYw3'
    consumer_secret = 'eEGaBsKs3Ojz85p6'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'



class MpesaAccessToken:
    access_token = ''

    def __init__(self) -> None:
        self.getAccessToken()
    def getAccessToken(self):
        
        r = requests.get(MpesaCredentials.api_URL, auth=HTTPBasicAuth(MpesaCredentials.consumer_key, MpesaCredentials.consumer_secret))
        mpesa_access_token = json.loads(r.text)
        validated_mpesa_access_token = mpesa_access_token['access_token']
        self.access_token = validated_mpesa_access_token
        return Response(validated_mpesa_access_token)


class LipaNaMpesaPass:
    lipa_time = datetime.now().strftime('%Y%m%d%H%M%S')
    Business_short_code = "174379"
    test_c2b_short_code = "600987"
    passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
    data_to_encode = Business_short_code + passkey + lipa_time
    online_password = base64.b64encode(data_to_encode.encode())
    decode_password = online_password.decode('utf-8')

class LipaNaMpesa:
    access_token = MpesaAccessToken().access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": "Bearer %s" % access_token}
    

    def __init__(self,amount,phoneNo,account) -> None:
        self.amount = amount
        self.phone_number = int(f'254{phoneNo}')
        self.account = account
        self.accepted = False

    def generate_password(self):
        passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
        lipa_time = datetime.now().strftime('%Y%m%d%H%M%S')

        data_to_encode = LipaNaMpesaPass.Business_short_code + passkey + lipa_time
        online_password = base64.b64encode(data_to_encode.encode())
        decode_password = online_password.decode('utf-8')
        return decode_password

    def lipa(self,request):
        request = {
        "BusinessShortCode": LipaNaMpesaPass.Business_short_code,
        "Password": self.generate_password(),
        "Timestamp": LipaNaMpesaPass.lipa_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": self.account,
        "PartyA": self.phone_number,  # replace with your phone number to get stk push
        "PartyB": LipaNaMpesaPass.Business_short_code,
        "PhoneNumber": self.phone_number,  # replace with your phone number to get stk push
        "CallBackURL": "",
        "AccountReference": self.account,
        "TransactionDesc": "Space Savings Update"
        }
        print(request)
        response = requests.post(self.api_url, json=request, headers=self.headers)
        return response
    
    @csrf_exempt
    def confirmation(self,request):
        mpesa_body =request.body.decode('utf-8')
        mpesa_payment = json.loads(mpesa_body)
        if mpesa_payment['body']['stkCallback']['ResultCode'] ==0:
            self.accepted = True
        else:
            self.accepted = False
        
        context = {
            "ResultCode": 0,
            "ResultDesc": "Accepted"
        }
        return Response(context)

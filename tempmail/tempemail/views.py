import random
import string
import requests
from django.http import JsonResponse
from django.views import View
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

class GenerateRandomMailbox(View):
    def get(self, request):
        # Generate a random username
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        domain = 'handykiller.com'  # Custom domain
        mailbox = f'{username}@{domain}'
        
        return JsonResponse({'mailbox': mailbox})

@method_decorator(csrf_exempt, name='dispatch')
class CheckMessages(View):
    def post(self, request):
        mailbox = request.POST.get('mailbox')
        login, domain = mailbox.split('@')
        
        url = 'https://www.1secmail.com/api/v1/'
        params = {
            'action': 'getMessages',
            'login': login,
            'domain': domain
        }
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            messages = response.json()
            if messages:
                latest_message_id = messages[0]['id']
                message_url = f'https://www.1secmail.com/api/v1/?action=readMessage&login={login}&domain={domain}&id={latest_message_id}'
                message_response = requests.get(message_url)
                if message_response.status_code == 200:
                    message = message_response.json()
                    return JsonResponse({'message': message})
            return JsonResponse({'message': 'No new messages'})
        else:
            return JsonResponse({'error': 'Failed to fetch messages'}, status=response.status_code)

def index(request):
    return render(request, 'index.html')

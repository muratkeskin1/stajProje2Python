from twilio.twiml.voice_response import VoiceResponse
from flask import Flask, request
import requests
import os
import openai
import azure.cognitiveservices.speech as speechsdk
from twilio.twiml.voice_response import VoiceResponse, Gather
import json

from twilio.rest import Client
app = Flask(__name__)

# Twilio'dan gelen arama isteğini işleme fonksiyonu
def process_voice_request(request):
    response = VoiceResponse()
    print(request.values)
    # Gelen sesli mesajı alın
    gather = Gather( input="speech", timeout="5", language="en-US",action="/voice",method="POST")
    gather.say('For sales, press 1. For support, press 2.')
    response.append(gather)

    # If the user doesn't select an option, redirect them into a loop
    #response.redirect('/voice')
    speech_result = request.form['SpeechResult']
    response.say(message="today is 18 may")
    return str("this is a test message") 
    # Gelen mesaja göre cevap oluşturun
    if 'merhaba' in speech_result.lower():
        response.say(message='Merhaba, nasıl yardımcı olabilirim?')
    elif 'teşekkür ederim' in speech_result.lower():
        response.say(message='Rica ederim, yardımcı olabileceğim başka bir konu var mı?')
    else:
        response.say(message='Anlamadım, lütfen tekrar eder misiniz?')
    # Gelen sesli mesajı alın
    return str(response)
# "/voice" yolunda POST isteği geldiğinde işleme fonksiyonunu çağırın
@app.route('/voice', methods=['POST'])
def voice():
    return process_voice_request(request)
# Telefon aramasını gerçekleştiren fonksiyon
def make_phone_call():
    account_sid = ''
    auth_token = ''
    from_number = '+'
    to_number = '+'

    client = Client(account_sid, auth_token)

    call = client.calls.create(
        url=' https://71ce-151-135-108-67.ngrok-free.app/voice',
        to=to_number,
        from_=from_number
    )

    print(call.sid)
@app.route('/gather', methods=['GET','POST'])
def user_input_gather():
    response = VoiceResponse()
    if 'Digits' in request.values:
        # Get which digit the caller chose
        choice = request.values['Digits']
        print("request : "+ request)
        
        # <Say> a different message depending on the caller's choice
        if choice == '1':
            response.say('You selected sales. Good for you!')
            return str(response)
        elif choice == '2':
            response.say('You need support. We will help!')
            return str(response)
        else:
            # If the caller didn't choose 1 or 2, apologize and ask them again
            response.say("Sorry, I don't understand that choice.")

    # If the user didn't choose 1 or 2 (or anything), send them back to /voice
    response.redirect('/voice')
    return str(response)

    gather = response.gather(
        input='speech', 
        timeout='5', 
        language='en-US', 
        action='/voice', 
        method='POST'
    )
    response.append(gather.to_xml())

    # Say a message to prompt the user for input
    gather.say("Please say something after the beep.")
    # If the user doesn't provide input, redirect to another URL
    response.redirect('/gather')

def azure_gpt_api(message):

    openai.api_type = "azure"

    openai.api_base = "/"

    openai.api_version = "2023-03-15-preview"

    openai.api_key =""

    response = openai.ChatCompletion.create(

    engine="",  

    messages = [{"role":"user","content":message}],

    temperature=0.7,

    max_tokens=150,

    top_p=0.95,

    frequency_penalty=0,

    presence_penalty=0,

    stop=None)

    return response

make_phone_call()
if __name__ == '__main__':
    app.run()

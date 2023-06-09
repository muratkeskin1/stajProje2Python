print("hello")


import requests
import os
import openai

import azure.cognitiveservices.speech as speechsdk
from twilio.twiml.voice_response import VoiceResponse, Gather
import json

from twilio.rest import Client

url="http://127.0.0.1:5000"
def twillio_call():

    TWILIO_PHONE_NUMBER = "+12543543707"


    # list of one or more phone numbers to dial, in "+19732644210" format

    DIAL_NUMBERS = ["+905318246769"]


    # URL location of TwiM  L instructions for how to handle the phone call

    TWIML_INSTRUCTIONS_URL ="http://static.fullstackpython.com/phone-calls-python.xml"


    # replace the placeholder values with your Account SID and Auth Token

    # found on the Twilio Console: https://www.twilio.com/console

    client = Client("AC5c6f128cdc17f83fe09bad7a5cbfbfdb", "d76733046a480d37d71d30a47e6867e0")
    for number in DIAL_NUMBERS:
        print("Dialing " + number)
        client.calls.create( url=url+"http://127.0.0.1:5000/voice",
                to="+905318246769",
                    from_="+12543543707")
twillio_call()

def azure_gpt_api(message):

    openai.api_type = "azure"

    openai.api_base = "https://interntprojectgpt.openai.azure.com/"

    openai.api_version = "2023-03-15-preview"

    openai.api_key ="bf5b957b0b564581ae2840150f2874b3"

    response = openai.ChatCompletion.create(

    engine="azuregpt",  

    messages = [{"role":"user","content":message}],

    temperature=0.7,

    max_tokens=800,

    top_p=0.95,

    frequency_penalty=0,

    presence_penalty=0,

    stop=None)

    return response

def text_to_speech_input(text):

    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"

    speech_config = speechsdk.SpeechConfig(subscription='e36d7f1d2bf74d13a8ee3cfd42676669', region='westeurope')

    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
    

    # The language of the voice that speaks.

    speech_config.speech_synthesis_voice_name='tr-TR-AhmetNeural'
    

    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    

    # Get text from the console and synthesize to the default speaker.

    #print("Enter some text that you want to speak >")

    #text = input()
    

    speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()
    

    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:

        print("Speech synthesized for text [{}]".format(text))

    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:

        cancellation_details = speech_synthesis_result.cancellation_details

        print("Speech synthesis canceled: {}".format(cancellation_details.reason))

        if cancellation_details.reason == speechsdk.CancellationReason.Error:

            if cancellation_details.error_details:

                print("Error details: {}".format(cancellation_details.error_details))

                print("Did you set the speech resource key and region values?")

   # return speech_config, audio_config, cancellation_details, text

def recognize_from_microphone():


    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"


    speech_config = speechsdk.SpeechConfig(subscription="e36d7f1d2bf74d13a8ee3cfd42676669", region="westeurope")


    speech_config.speech_recognition_language="en-US"



    #audio_config = speechsdk.audio.AudioConfig(filename="beklebekle.m4a")


    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)


    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)



    print("Speak into your microphone.")


    speech_recognition_result = speech_recognizer.recognize_once_async().get()


    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:


        print("Recognized: {}".format(speech_recognition_result.text))


        return speech_recognition_result.text


    elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:


        print("No speech could be recognized: {}".format(speech_recognition_result.no_match_details))


    elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:

        cancellation_details = speech_recognition_result.cancellation_details


        print("Speech Recognition canceled: {}".format(cancellation_details.reason))


        if cancellation_details.reason == speechsdk.CancellationReason.Error:


            print("Error details: {}".format(cancellation_details.error_details))


            print("Did you set the speech resource key and region values?")



#recognize_from_microphone()


# Sesli girişin metne dönüştürülmesi için kullanılacak konuşma tanıma API'si


def speech_to_text():


    # Konuşma tanıma API'si çağrısı yapılır ve audio_file ses dosyası üzerinde işlem yapılır


    # Sonuç olarak metin bir dize olarak elde edilir


    # TODO: Konuşma tanıma API'si çağrısını burada gerçekleştirin
  


    text =  recognize_from_microphone()  # Örnek olarak sabit bir metin döndürüyoruz


    return text



# Metni sesli yanıta dönüştürmek için kullanılacak metin-konuşma API'si


def text_to_speech(text):


    # Metin-konuşma API'si çağrısı yapılır ve text metni sesli bir şekilde çevrilir


    # Sonuç olarak ses dosyası elde edilir


    # TODO: Metin-konuşma API'si çağrısını burada gerçekleştirin


    audio_file = "response.wav"  # Örnek olarak bir ses dosyası adı döndürüyoruz
    return audio_file



# ChatGPT API'sine metin girişi göndererek yanıt almak


def get_chat_response(message):


    url = "https://api.openai.com/v1/chat/completions"


    headers = {


        "Content-Type": "application/json",


        "Authorization": "Bearer YOUR_API_KEY"


    }


    payload = {


        "model": "gpt-3.5-turbo",


        "messages": [{"role": "system", "content": "You are a call bot."}, {"role": "user", "content": message}],


        "temperature": 0.7


    }


    response = requests.post(url, headers=headers, json=payload)


    data = response.json()


    chat_response = data["choices"][0]["message"]["content"]
    return chat_response



# Sesli giriş al


#audio_file = "input.wav"  # Örnek olarak bir ses dosyası adı kullanıyoruz


#text_input = speech_to_text()


#print(text_input)

#text_to_speech_input()
def gpt_loop():
    while(True):
        print("enter your message or exit with press x")
        message=input()
        if message=="x":
            break
        f = open('info.json')
        data = str(json.load(f))
        response=azure_gpt_api(message)
        print(response.choices[0].message.content)
        text_to_speech_input(str(response.choices[0].message.content))
# Metin girişini ChatGPT API'sine göndererek yanıt al


#chat_response = get_chat_response(text_input)


# Metin yanıtını sesli olarak çevir


#audio_response = text_to_speech(chat_response)


twillio_call()


# Sesli yanıtı kullanıcıya iletmek için gerekli işlemleri yap


# TODO: Sesli yanıtı kullanıcıya iletmek için gerekli adımları burada gerçekleştirin



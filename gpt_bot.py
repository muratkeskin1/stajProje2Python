from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Gather
import openai
import time

# Twilio hesap bilgileri
account_sid = ''
auth_token = ''
twilio_phone_number = ''
twiml_url=""
openAi_key=""
initial_message="Sen yeni araba arayan bir yapay zeka asistanısın ve ben araba satıcısıyım bana bununla ilgili kısa  sorular sor tek cümlelik olsun sorular."
initial_message_2="Sen  almak için araba arayan bir yapay zeka asistanısın ve ben araba satıcısıyım bana bununla ilgili tek cümlelik sorular"
# Kullanıcıdan gelen sesli girişi işleyen fonksiyon
def write_file(data):
    f = open("data.txt", "a")   
    f.write(data)
    f.close()
        
def read_file():
    f = open('data.txt', 'r')
    return f.read()

def process_speech(speech_result):
    response = VoiceResponse()
    print("speech: "+str(speech_result))
    write_file("user: "+str(speech_result)+ " \n")
    # Kullanıcının girişine göre cevap oluşturma
    if speech_result is None:
        answer= azure_gpt_api("elimde audi araba var şuan")
        gather = Gather(input="speech", action_on_empty_result="true" ,timeout=15, language="tr-TR", action="/process_speech", method="POST")
        gather.say(message='Anlamadım, lütfen tekrar eder misiniz', voice="Polly.Filiz",language="tr-TR")
        response.append(gather)
    elif 'bitir' in speech_result.lower():
        response.say(message="konuşmayı sonlandırılıyor.", voice="Polly.Filiz",language="tr-TR")
        return str(response)
    else:
        answer=azure_gpt_api(speech_result)
        print("answer: "+answer.choices[0].message.content)
        write_file("bot: "+ str(answer.choices[0].message.content)+ " \n")
        #response.say(answer)
        gather = Gather(input="speech", action_on_empty_result="true" ,timeout=15, language="tr-TR", action="/process_speech", method="POST")
        gather.say(message=answer.choices[0].message.content,voice="Polly.Filiz",language="tr-TR")
        response.append(gather)
    #response.redirect("/gather")
    return str(response)

# Arama yapma fonksiyonu
def make_outbound_call(to_number):
    client = Client(account_sid, auth_token)

    call = client.calls.create(
        #twiml='<Response><Gather input="speech" timeout="5" language="tr-TR"  action="https://5f43-5-46-207-39.ngrok-free.app/process_speech" method="POST"><Say>Bir şey söyleyin.</Say></Gather></Response>',
        to=to_number,
        from_=twilio_phone_number,
        url=twiml_url
    )

    print('Arama SID:', call.sid)

# /process_speech endpoint'i için işleme fonksiyonu
def process_speech_request():
    print("request form "+str(request.form))
    print("speech result "+str(request.form.get('SpeechResult')))
    speech_result=request.form.get('SpeechResult')
    #speech_result = request.form['SpeechResult']
    response = process_speech(speech_result)
    return response
def azure_gpt_api(message):

    openai.api_type = "azure"

    openai.api_base = "https://interntprojectgpt.openai.azure.com/"

    openai.api_version = "2023-03-15-preview"

    openai.api_key =openAi_key

    response = openai.ChatCompletion.create(

    engine="azuregpt",  

    messages = [{"role":"user","content":message}],

    temperature=0.7,

    max_tokens=150,

    top_p=0.95,

    frequency_penalty=0,

    presence_penalty=0,

    stop=None)

    return response


# Flask uygulaması oluşturma
from flask import Flask, request,render_template,Response,redirect

app = Flask(__name__)

@app.route('/gather',methods=['POST'])
def gather_process():
    gather = Gather(input="speech", action_on_empty_result="true" ,timeout=5, language="tr-TR", action="/process_speech", method="POST")
    gather.say(first_message_initial)
    response.append(gather)
@app.route('/', methods=['GET'])
def main():
    return render_template("main.html", content=read_file())
@app.route('/get_file', methods=['GET'])
def file():
    return read_file()
@app.route('/gpt', methods=['GET'])
def gpt():
    return azure_gpt_api("this is a test message").choices[0].message.content

def stream_file_content():
    count = 0
    while True:
        content = read_file()
        yield content
        time.sleep(1)
@app.route('/update_file', methods=['POST'])
def update():
    name = request.form['name']
    phone = request.form['phone']
    action = request.form['action']

    # Verileri dosyaya ekleme veya silme
    with open('phone_numbers.txt', 'a+') as file:
        if action == 'add':
            file.write(f'{name},{phone}\n')
        elif action == 'remove':
            file.seek(0)
            lines = file.readlines()
            file.truncate(0)
            for line in lines:
                if f'{name},{phone}' not in line:
                    file.write(line)
    return redirect('/table')
@app.route('/table')
def index():
    # Verileri dosyadan oku
    data = []
    with open('phone_numbers.txt', 'r') as file:
        for line in file:
            data.append(line.strip().split(','))
    return render_template('phone_list.html', data=data)
@app.route('/stream')
def stream():
   return Response (stream_file_content(), mimetype='text/plain')
# /voice endpoint'i için çağrı işleme fonksiyonu
@app.route('/voice', methods=['POST'])  
def voice():
    response = VoiceResponse()
    prefix='+'
    phone_number=str(request.args.get('phone'))
    phone=prefix+phone_number.strip()
    make_outbound_call(phone)
    first_message_initial=azure_gpt_api(initial_message_2)
    gather = Gather(input="speech", action_on_empty_result="true" ,timeout=20, language="tr-TR", action="/process_speech", method="POST")
    gather.say(message=first_message_initial.choices[0].message.content, voice="Polly.Filiz",language="tr-TR")
    response.append(gather)
    return str(response)
# /process_speech endpoint'i için çağrı işleme fonksiyonu
@app.route('/process_speech', methods=['POST'])
def process_speech_route():
    print("proceess_speech_route")
    return process_speech_request()
@app.route('/test_url', methods=['POST'])
def process_speech_route1():
    prefix='+'
    phone_number=str(request.args.get('phone'))
    phone=prefix+phone_number.strip()
    print(phone)
    return str(phone_number)
if __name__ == '__main__':
    app.run(debug=True)

from twilio.twiml.voice_response import VoiceResponse
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import openai
import json
import openai
# Set up the OpenAI API with the API key
configuration = openai.Configuration(api_key="YOUR_OPENAI_API_KEY")
openai.api_client.configuration = configuration

def handler(context, event):
    # Set up the Twilio VoiceResponse object to generate the TwiML
    twiml = VoiceResponse()

    # Initiate the Twilio Response object to handle updating the cookie with the chat history
    response = MessagingResponse()

    # Parse the cookie value if it exists
    cookie_value = event['request']['cookies'].get('convo')
    cookie_data = json.loads(urllib.parse.unquote(cookie_value)) if cookie_value else None

    # Get the user's voice input from the event
    voice_input = event.get('SpeechResult')

    # Create a conversation variable to store the dialog and the user's input to the conversation history
    conversation = cookie_data['conversation'] if cookie_data and 'conversation' in cookie_data else []
    conversation.append(f"user: {voice_input}")

    # Get the AI's response based on the conversation history
    ai_response = generate_ai_response(';'.join(conversation))

    # For some reason the OpenAI API loves to prepend the name or role in its responses, so let's remove 'assistant:' 'Joanna:', or 'user:' from the AI response if it's the first word
    cleaned_ai_response = re.sub(r"^\w+:\s*", "", ai_response).strip()
    # Add the AI's response to the conversation history
    conversation.append(f"assistant: {ai_response}")

    # Limit the conversation history to the last 10 messages; you can increase this if you want but keeping things short for this demonstration improves performance
    while len(conversation) > 10:
        conversation.pop(0)

    # Generate some <Say> TwiML using the cleaned up AI response
    twiml.say(cleaned_ai_response, voice='Polly.Joanna-Neural')

    # Redirect to the Function where the <Gather> is capturing the caller's speech
    twiml.redirect('/transcribe', method='POST')

    # Since we're using the response object to handle cookies we can't just pass the TwiML straight back to the callback, we need to set the appropriate header and return the TwiML in the body of the response
    response.append_header('Content-Type', 'application/xml')
    response.set_body(str(twiml))

    # Update the conversation history cookie with the response from the OpenAI API
    new_cookie_value = urllib.parse.quote(json.dumps({'conversation': conversation}))
    response.set_cookie('convo', new_cookie_value, path='/')

    # Return the response to the handler
    return response

# Function to generate the AI response based on the conversation history
def generate_ai_response(conversation):
    messages = format_conversation(conversation)
    return create_chat_completion(messages)

# Function to create a chat completion using the OpenAI API
def create_chat_completion(messages):
    completion = azure_gpt_api(message)
    return completion.choices[0].message.content

# Function to format the conversation history into a format that the OpenAI API can understand
def format_conversation(conversation):
    messages = [
        {"role": "system", "content": "You are a creative, funny, friendly and amusing AI assistant named Joanna. Please provide engaging but concise responses."},
        {"role": "user", "content": "We are having a casual conversation over the telephone so please provide engaging but concise responses."}
    ]

    for message in conversation.split(";"):
        role = "assistant" if messages[-1]["role"] == "user" else "user"
        messages.append({"role": role, "content": message.strip()})

    return messages
def azure_gpt_api(message):

    openai.api_type = "azure"

    openai.api_base = "/"

    openai.api_version = "2023-03-15-preview"

    openai.api_key =""

    response = openai.ChatCompletion.create(

    engine="",  

    messages = [{"role":"user","content":message}],

    temperature=0.7,

    max_tokens=800,

    top_p=0.95,

    frequency_penalty=0,

    presence_penalty=0,

    stop=None)

    return response

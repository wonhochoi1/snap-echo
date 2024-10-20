import reflex as rx
import google.generativeai as genai
import os

# genai.configure(api_key=os.environ["GOOGLE_KEY"])
genai.configure(api_key="AIzaSyA_MV25oMNBn3zmRZFQ56WnYMsJdjPQGuU")



from dotenv import load_dotenv
from time import sleep
import logging
from deepgram.utils import verboselogs
from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    LiveTranscriptionEvents,
    LiveOptions,
    Microphone,
)
from pymongo import MongoClient

load_dotenv()

# MongoDB connection
MONGO_KEY='mongodb+srv://ishansheth31:Kevi5han1234@breezytest1.saw2kxe.mongodb.net/'
client = MongoClient(MONGO_KEY)
db = client['textstorage']  # Replace with your actual DB name
collection = db['test1']  # Collection where utterances will be stored

is_finals = []


API_KEY = "7d3c88e5c2d1ed6533d6bfa4123ac2adc1c8f200"
deepgram: DeepgramClient = DeepgramClient(API_KEY)

def on_open(self, open, **kwargs):
    print("Connection Open")

def on_message(self, result, **kwargs):
    global is_finals
    sentence = result.channel.alternatives[0].transcript
    if len(sentence) == 0:
        return
    if result.is_final:
        print(f"Message: {result.to_json()}")
        is_finals.append(sentence)

        if result.speech_final:
            utterance = " ".join(is_finals)
            print(f"Speech Final: {utterance}")
            
            # Insert utterance into MongoDB
            collection.insert_one({"utterance": utterance})

            # Clear the finals list
            is_finals = []
        else:
            print(f"Is Final: {sentence}")
    else:
        print(f"Interim Results: {sentence}")

def on_metadata(self, metadata, **kwargs):
    print(f"Metadata: {metadata}")

def on_speech_started(self, speech_started, **kwargs):
    print("Speech Started")

def on_utterance_end(self, utterance_end, **kwargs):
    print("Utterance End")
    global is_finals
    if len(is_finals) > 0:
        utterance = " ".join(is_finals)
        print(f"Utterance End: {utterance}")

        # Insert utterance into MongoDB
        collection.insert_one({"utterance": utterance})

        is_finals = []

def on_close(self, close, **kwargs):
    print("Connection Closed")

def on_error(self, error, **kwargs):
    print(f"Handled Error: {error}")

def on_unhandled(self, unhandled, **kwargs):
    print(f"Unhandled Websocket Message: {unhandled}")

dg_connection = deepgram.listen.live.v("1")
dg_connection.on(LiveTranscriptionEvents.Open, on_open)
dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)
dg_connection.on(LiveTranscriptionEvents.Metadata, on_metadata)
dg_connection.on(LiveTranscriptionEvents.SpeechStarted, on_speech_started)
dg_connection.on(LiveTranscriptionEvents.UtteranceEnd, on_utterance_end)
dg_connection.on(LiveTranscriptionEvents.Close, on_close)
dg_connection.on(LiveTranscriptionEvents.Error, on_error)
dg_connection.on(LiveTranscriptionEvents.Unhandled, on_unhandled)

options: LiveOptions = LiveOptions(
    model="nova-2",
    language="en-US",
    smart_format=True,
    encoding="linear16",
    channels=1,
    sample_rate=16000,
    interim_results=True,
    utterance_end_ms="1000",
    vad_events=True,
    endpointing=300,
)

addons = {
    "no_delay": "true"
}

import datetime

class State(rx.State):
    """The app state."""
    transcriptions: list[str] = []
    hasRecorded: bool = False
    isRecording: bool = False
    fullTranscript: str = ""  # We'll store the entire transcript here
    keyPoints: str = ""
    actionItems: str = ""
    recordingDate: str = ""
    recordingDuration: str = ""
    bookmarks: str = ""

    def fetch_transcript(self):
        combined_transcript = ""
        try:
            documents = collection.find().sort("_id")
            
            for document in documents:
                print(f"Document: {document}")  # Debugging log
                combined_transcript += document['utterance'] + "\n"

            # Update state with the combined transcript
            self.fullTranscript = combined_transcript
            print(f"Fetched Transcript: {self.fullTranscript}")  # Debugging log
            
            # Ensure analyze_transcript is called after the transcript is fetched
            self.analyze_transcript()  # Moved here to ensure transcript is ready
            self.fetch_bookmarks()
            
        except Exception as e:
            print(f"Error fetching transcript: {e}")  # Catch and log any errors
    
    def fetch_bookmarks(self):
        try:
            self.bookmarks = """
            1 - This is a test.\n
            2 - I hate Hwan Ho Choi\n
            3 - Cheetos Cheetos\n
            """
        except Exception as e:
            print(f"Error fetching transcript: {e}")  # Catch and log any errors


    def analyze_transcript(self): 
        """Analyze the transcript and generate a summary with action items."""
        model = genai.GenerativeModel("gemini-1.5-flash")
        print("Full transcript: " +self.fullTranscript)
        # Generate key discussion points summary
        summary_response = model.generate_content(
            f"Summarize this meeting in 10-15 bullet and sub-bullet points IN YOUR OWN WORDS. Organize main bullets by topic and have sub bullets. Be as detailed as possible. Make each point in a separate line and ensure bullets: {self.fullTranscript}. Say Summary: at the beginning with hyphen bullets, no markdown or **. At the very beginning, give a 2 sentence overview, 2 line breaks, and then do the summary part"
        )
        self.keyPoints = summary_response.text

        # Generate action items from the conversation
        action_items_response = model.generate_content(
            f"List all action items from this meeting transcript. Each action item should be in bullet points and a new line: {self.fullTranscript}"
        )
        self.actionItems = action_items_response.text

        print(f"Generated Key Points: {self.keyPoints}")
        print(f"Generated Action Items: {self.actionItems}")

    def start_recording(self):
        self.isRecording = True
        print("\n\nPress Enter to stop recording...\n\n")
        if dg_connection.start(options, addons=addons) is False:
            print("Failed to connect to Deepgram")
            return

        global microphone
        microphone = Microphone(dg_connection.send)
        microphone.start()

    def stop_recording(self):
        self.isRecording = False
        microphone.finish()
        dg_connection.finish()
        self.hasRecorded = True
        print("Finished")

import speech_recognition as sr
from colorama import Fore, Style
import spacy
import nltk
nltk.download('stopwords')
nltk.download('punkt')

# Initialize speech recognition
recognizer = sr.Recognizer()

# Define keywords to highlight
keywords_to_highlight = ["graining", "degradation", "pit window", "box", "traffic", "clear air"]

# Load English tokenizer, tagger, parser, NER and word vectors
nlp = spacy.load("en_core_web_sm")

# Start listening to the microphone
with sr.Microphone() as source:
    while True:  # this will keep running until you stop the program
        print("Listening...")
        audio = recognizer.record(source, duration=3)  # listen for the first 5 seconds

        try:
            # Use Google's Speech-to-Text API to convert the audio to text
            text = recognizer.recognize_google(audio)
            print("You said: " + text)

            # Split the text and the keywords into words
            text_words = set(text.lower().split())
            keyword_words = {word for keyword in keywords_to_highlight for word in keyword.split()}

            # Check for keywords and highlight them
            found_keywords = keyword_words & text_words
            if found_keywords:
                print(Fore.RED + "Highlighted words found in the audio:", ", ".join(found_keywords) + Style.RESET_ALL)

            # Process whole documents
            doc = nlp(text)

            # Analyze syntax
            noun_phrases = [chunk.text for chunk in doc.noun_chunks]
            print("Noun phrases:", noun_phrases)

            # Named entities, phrases and concepts
            for entity in doc.ents:
                print(entity.text, entity.label_)

        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
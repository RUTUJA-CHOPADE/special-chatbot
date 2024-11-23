import nltk
import random
from textblob import TextBlob
import speech_recognition as sr

# Initialize NLTK resources
nltk.download('punkt')

# Define motivational quotes
motivational_quotes = [
    "Believe in yourself! You are capable of amazing things.",
    "Keep going, you're doing great!",
    "Don't give up, you're closer than you think.",
    "You have the power to change your life.",
    "Success is the sum of small efforts, repeated day in and day out.",
    "You are stronger than you think!"
]

# Define a function for the chatbot with personalization, sentiment analysis, context-awareness, and speech recognition
class SpecialChatbot:
    def __init__(self):
        self.user_name = None
        self.user_mood = None
        self.context = []

    def get_sentiment(self, text):
        # Perform sentiment analysis using TextBlob
        analysis = TextBlob(text)
        # Return sentiment polarity (-1 to 1, where -1 is negative, 1 is positive)
        return analysis.sentiment.polarity

    def recognize_speech(self):
        # Initialize recognizer
        recognizer = sr.Recognizer()

        # Capture the audio from the microphone
        with sr.Microphone() as source:
            print("Listening for your input... (Speak now)")
            recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
            try:
                audio = recognizer.listen(source, timeout=5)  # timeout to avoid indefinite waiting
                print("Audio captured, processing...")
                text = recognizer.recognize_google(audio)
                print(f"You said: {text}")
                return text
            except sr.UnknownValueError:
                print("Sorry, I could not understand your speech.")
                return None
            except sr.RequestError:
                print("Could not request results; check your network connection.")
                return None
            except Exception as e:
                print(f"Error during speech recognition: {e}")
                return None

    def respond(self, user_input):
        # Check if the user is asking for their name
        if "name" in user_input.lower():
            if self.user_name:
                return f"Your name is {self.user_name}."
            else:
                return "I don't know your name yet. What's your name?"
        
        # Store the user's name
        if self.user_name is None and "my name is" in user_input.lower():
            self.user_name = user_input.split("is")[-1].strip()
            return f"Nice to meet you, {self.user_name}!"
        
        # Analyze sentiment
        sentiment = self.get_sentiment(user_input)
        if sentiment > 0:
            mood = "positive"
        elif sentiment < 0:
            mood = "negative"
        else:
            mood = "neutral"
        
        self.user_mood = mood
        # Add input to context for context-awareness
        self.context.append(user_input)
        
        # Respond based on sentiment and context
        if "hello" in user_input.lower():
            return f"Hello, {self.user_name if self.user_name else 'there'}! How are you feeling today?"
        
        elif "bye" in user_input.lower():
            return f"Goodbye, {self.user_name if self.user_name else 'friend'}! It was nice chatting with you."
        
        elif self.user_mood == "positive":
            return "I'm glad you're feeling good! Tell me more."
        
        elif self.user_mood == "negative":
            # Provide a unique motivational response when the user is feeling negative
            return random.choice(motivational_quotes)
        
        else:
            return random.choice([
                "Tell me more!",
                "Interesting, go on.",
                "I see, what else?"
            ])

    def chat(self):
        print("Hello! I'm your special chatbot. Type 'bye' to end the conversation.")
        while True:
            # Get user input via speech or text
            user_input = input(f"{self.user_name if self.user_name else 'You'}: ")

            if user_input.lower() == "speech":
                # If the user types 'speech', we activate speech recognition
                user_input = self.recognize_speech()
                if user_input is None:
                    continue
            
            # If user says 'bye', end the conversation
            if user_input.lower() == "bye":
                print(self.respond(user_input))
                break
            else:
                # Get chatbot response
                response = self.respond(user_input)
                print(f"Chatbot: {response}")

# Run the chatbot
if __name__ == "__main__":
    chatbot = SpecialChatbot()
    chatbot.chat()

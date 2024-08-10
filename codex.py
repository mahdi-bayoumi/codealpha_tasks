import wikipedia
import webbrowser
import datetime
import sys
import smtplib
from playsound import playsound
from helperF import *
from news import speak_news
from youtube import youtube
from sys import platform
import warnings
from facerecogn.Facerecog import run_face_recognition
from questionsandanswers import *

warnings.filterwarnings("ignore", category=SyntaxWarning)

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()
engine.setProperty('voice', engine.getProperty('voices')[0].id)

known_people = {
    "steve jobs": "Steve Jobs was the co-founder of Apple Inc. and a pioneer of the personal computer revolution.",
    "albert einstein": "Albert Einstein was a theoretical physicist who developed the theory of relativity.",
    "marie curie": "Marie Curie was a physicist and chemist who conducted pioneering research on radioactivity.",
    "nelson mandela": "Nelson Mandela was a South African anti-apartheid revolutionary and political leader.",
    "isaac newton": "Isaac Newton was an English mathematician, physicist, astronomer, and author who is widely recognized as one of the most influential scientists of all time.",
    "elon musk": "Elon Musk is the founder of Tesla and SpaceX, and a key figure in advancing electric vehicles and space exploration."
}


def speak(audio):
    """Convert text to speech."""
    engine.say(audio)
    engine.runAndWait()


def play_and_print_music(folder_path):
    if not os.path.isdir(folder_path):
        print(f"Error: Invalid folder path: {folder_path}")
        return

    for filename in os.listdir(folder_path):
        if filename.endswith((".mp3", ".wav", ".flac")):
            speak(f"Playing: {filename}")
            playsound(os.path.join(folder_path, filename))


class Codex:
    def __init__(self):
        self.chrome_path = None
        self.set_browser_path()
        self.knowledge_file = 'codex_knowledge.json'
        self.knowledge = {}
        self.load_knowledge()

    def set_browser_path(self):
        """Set the path for the default web browser based on the OS."""
        if platform == "linux" or platform == "linux2":
            self.chrome_path = '/usr/bin/google-chrome'
        elif platform == "darwin":
            self.chrome_path = 'open -a /Applications/Google Chrome.app'
        elif platform == "win32":
            self.chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
        else:
            print('Unsupported OS')
            sys.exit(1)
        webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(self.chrome_path))

    def load_knowledge(self):
        """Load knowledge from a JSON file."""
        if os.path.exists(self.knowledge_file):
            try:
                with open(self.knowledge_file, 'r') as f:
                    content = f.read()
                    self.knowledge = json.loads(content) if content.strip() else {}
            except (FileNotFoundError, json.JSONDecodeError):
                print(f"Error: Could not load knowledge from {self.knowledge_file}. Initializing empty knowledge base.")
        else:
            self.save_knowledge()

    def save_knowledge(self):
        """Save the current knowledge to a JSON file."""
        with open(self.knowledge_file, 'w') as f:
            json.dump(self.knowledge, f, indent=2)

    def learn(self, key, value):
        """Learn a new fact."""
        self.knowledge[key] = value
        self.save_knowledge()
        speak(f"I've learned that {key} is {value}")

    def clear_knowledge(self):
        """Clear all stored knowledge."""
        self.knowledge = {}
        self.save_knowledge()
        speak("I have cleared all my learned knowledge.")

    def display_knowledge(self):
        """Display all stored knowledge."""
        if self.knowledge:
            speak("Here's what I've learned:")
            for key, value in self.knowledge.items():
                speak(f"{key} is {value}")
        else:
            speak("I haven't learned anything yet.")

    def recall(self, key):
        """Recall a fact from memory."""
        if key in self.knowledge:
            speak(f"I remember that {key} is {self.knowledge[key]}")
        else:
            speak(f"I don't have any information about {key}")

    @staticmethod
    def wishMe():
        """Greet the user based on the time of day."""
        hour = datetime.datetime.now().hour
        if 0 <= hour < 12:
            speak("Good Morning, sir.")
        elif 12 <= hour < 18:
            speak("Good Afternoon, sir.")
        else:
            speak('Good Evening, sir.')
        speak('I am Codex. Please tell me how can I help you, sir?')

    @staticmethod
    def sendEmail(to, content):
        """Send an email (requires setting up your email credentials)."""
        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.ehlo()
                server.starttls()
                server.login('email', 'password')
                server.sendmail('email', to, content)
                server.close()
            speak("Email has been sent.")
        except Exception as e:
            speak("Sorry, I am unable to send the email.")
            print(f"Error: {e}")

    def execute_query(self, query):
        query.lower()
        """Execute a command based on the user's query."""
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace('wikipedia', '')
            try:
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                print(results)
                speak(results)
            except Exception as e:
                speak("Sorry, I couldn't fetch results from Wikipedia.")
                print(f"Error: {e}")
        elif 'weather' in query:
            speak("Please tell me the city name.")
            city = takeCommand().lower()
            weather_info = get_weather(city)
            speak(f"The current weather in {city} is {weather_info}")

        elif 'news' in query:
            speak("Fetching the latest news headlines...")
            headlines = speak_news()
            for headline in headlines:
                speak(headline)

        elif 'set reminder' in query:
            speak("What should I remind you about?")
            reminder = takeCommand().lower()
            speak("When should I remind you?")
            reminder_time = takeCommand().lower()  # Process this input to schedule the reminder
            set_reminder(reminder, reminder_time)
            speak(f"Reminder set for {reminder_time} to {reminder}")

        elif 'motivation' in query:
            quotes = [
                "The only way to do great work is to love what you do. - Steve Jobs",
                "Success is not how high you have climbed, but how you make a positive difference to the world.",
                "Your limitation—it's only your imagination.",
                "Do not wait to strike till the iron is hot; but make it hot by striking. - William Butler Yeats",
                "The best way to predict the future is to invent it. - Alan Kay",
                "You miss 100% of the shots you don't take. - Wayne Gretzky",
                "Whether you think you can or think you can't, you're right. - Henry Ford",
                "The purpose of our lives is to be happy. - Dalai Lama",
                "Believe you can and you're halfway there. - Theodore Roosevelt",
                "Act as if what you do makes a difference. It does. - William James",
                "The only limit to our realization of tomorrow is our doubts of today. - Franklin D. Roosevelt",
                "Don’t watch the clock; do what it does. Keep going. - Sam Levenson",
                "Keep your face always toward the sunshine—and shadows will fall behind you. - Walt Whitman",
                "What lies behind us and what lies before us are tiny matters compared to what lies within us. - Ralph Waldo Emerson",
                "Happiness is not something ready-made. It comes from your own actions. - Dalai Lama",
                "The best way to get started is to quit talking and begin doing. - Walt Disney",
                "Don’t let yesterday take up too much of today. - Will Rogers",
                "You learn more from failure than from success. Don’t let it stop you. Failure builds character. - Unknown",
                "It’s not whether you get knocked down, it’s whether you get up. - Vince Lombardi",
                "If you are working on something that you really care about, you don’t have to be pushed. The vision pulls you. - Steve Jobs",
                "People who are crazy enough to think they can change the world, are the ones who do. - Rob Siltanen",
                "We may encounter many defeats but we must not be defeated. - Maya Angelou",
                "Knowing is not enough; we must apply. Wishing is not enough; we must do. - Johann Wolfgang Von Goethe"
            ]

            speak(random.choice(quotes))
        elif any(person in query for person in known_people):
            person = next((p for p in known_people if p in query), None)
            if person:
                speak(known_people[person])
            else:
                speak("Sorry, I don't have information about this person.")

        elif 'open notepad' in query:
            speak("Opening Notepad...")
            os.system("notepad.exe")

        elif 'search google' in query:
            speak("What should I search for?")
            search_query = takeCommand().lower()
            webbrowser.get('chrome').open_new_tab(f'https://www.google.com/search?q={search_query}')
        elif 'cpu' in query:
            speak(cpu())
        elif 'take' in query and 'screenshot' in query:
            screenshot()
        elif 'show' in query and 'screenshot' in query:
            showscreenshot()
        elif 'define' in query:
            speak("What word would you like defined?")
            word = takeCommand().lower()
            definition = get_definition(word)  # You would implement this function
            speak(f"The definition of {word} is {definition}")

        elif 'math problem' in query:
            speak("Please tell me the math problem.")
            math_problem = takeCommand().lower()
            try:
                result = eval(math_problem)
                speak(f"The result is {result}")
            except:
                speak("Sorry, I couldn't calculate that.")

        elif 'recipe' in query:
            speak("What recipe are you looking for?")
            recipe = takeCommand().lower()
            recipe_details = search_recipe(recipe)  # Implement this to fetch recipe details
            speak(recipe_details)

        elif 'currency conversion' in query:
            speak("Which currency would you like to convert?")
            currency_from = takeCommand().lower()
            speak("And to which currency?")
            currency_to = takeCommand().lower()
            speak("How much would you like to convert?")
            amount = takeCommand().lower()
            conversion = convert_currency(currency_from, currency_to, amount)  # Implement this function
            speak(f"{amount} {currency_from} is equal to {conversion} {currency_to}")

        elif 'clear knowledge' in query or 'forget everything' in query:
            speak("Are you sure you want me to forget all learned knowledge? This action cannot be undone.")
            confirmation = takeCommand().lower()
            if 'yes' in confirmation or 'sure' in confirmation:
                self.clear_knowledge()
            else:
                speak("Knowledge clearing cancelled.")
        elif 'your master' in query or 'creator' in query:
            speak("my master nickname is Codex,he is my Creator")
        elif 'help' in query or 'hello' in query:
            speak("yes hear i am, what I can help you, sir?")
        elif ' the time' in query:
            times = datetime.datetime.now().strftime('%I:%M %p')
            speak(f'The current time is {times}')
        elif 'who is' in query:
            person = query.replace('who is', '')
            speak(wikipedia.summary(person, sentences=1))
        elif 'joke' in query:
            speak(pyjokes.get_joke())

        elif 'display knowledge' in query or 'show what you know' in query:
            self.display_knowledge()

        elif 'youtube downloader' in query:
            exec(open('youtube_downloader.py').read())

        elif 'open youtube' in query:
            webbrowser.get('chrome').open_new_tab('https://youtube.com')

        elif 'open google' in query:
            webbrowser.get('chrome').open_new_tab('https://google.com')

        elif 'play music' in query:
            if 'youtube' in query:
                speak("What music would you like to listen to?")
                youtube(takeCommand().lower())
            else:
                folder_path = r"D:\music\2nashid"
                play_and_print_music(folder_path)

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")

        elif 'learn' in query:
            speak("What should I learn?")
            learn_key = takeCommand()
            if learn_key != '':
                speak(f"What is {learn_key}?")
                learn_value = takeCommand().lower()
                self.learn(learn_key, learn_value)

        elif 'recall' in query or 'remember' in query:
            speak("What should I recall?")
            recall_key = takeCommand().lower()
            self.recall(recall_key)

        elif 'forget' in query:
            speak("What should I forget?")
            forget_key = takeCommand().lower()
            if forget_key in self.knowledge:
                del self.knowledge[forget_key]
                self.save_knowledge()
                speak(f"I've forgotten about {forget_key}")
            else:
                speak(f"I don't have any information about {forget_key}")

        elif 'sleep' in query:
            speak("Goodbye, sir. Have a nice day!")
            sys.exit()

        elif 'tools you use' in query:
            speak("My master added to coding open ai nylas in addition to python libraries to make my response more accurate and to enhance speach recognition.")


def wakeUpCODEX():
    """Initialize Codex and start listening for commands."""
    bot = Codex()
    bot.wishMe()
    while True:
        query = takeCommand().lower()
        if query:
            bot.execute_query(query)


if __name__ == '__main__':
    recognized_name, is_new = run_face_recognition()
    if is_new:
        print("New user detected!")
    else:
        print(f"Welcome back, {recognized_name}!")
        wakeUpCODEX()

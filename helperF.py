import pyttsx3
import pyautogui
import psutil
import pyjokes
import requests
import speech_recognition as sr
import json
import geocoder
from difflib import get_close_matches
from PIL import Image
import random
import string
import os
import logging
import datetime
import time
import threading


logging.basicConfig(level=logging.ERROR)
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
g = geocoder.ip('me')
data = json.load(open(r'C:\Users\mahdi\PycharmProjects\Codex\data.json'))


def speak(audio) -> None:
    engine.say(audio)
    engine.runAndWait()


def generate_random_filename(length=10, prefix="", suffix=""):
    """
  Generates a random filename with a specified length, prefix, and suffix.

  Args:
      length (int, optional): The length of the random character sequence. Defaults to 10.
      prefix (str, optional): A string to prepend to the filename. Defaults to "".
      suffix (str, optional): A string to append to the filename (e.g., ".txt"). Defaults to "".

  Returns:
      str: The generated random filename.
  """

    # Define characters allowed in the filename
    allowed_chars = string.ascii_lowercase + string.digits

    # Generate random characters
    random_chars = ''.join(random.choice(allowed_chars) for _ in range(length))

    # Combine filename parts
    filename = f"{prefix}{random_chars}{suffix}"

    return filename


def get_latest_file(folder_path):
    """
  Identifies the most recently modified file in a given folder.

  Args:
      folder_path (str): The path to the folder to search.

  Returns:
      str: The path to the most recently modified file, or None if no files are found.
  """

    # Initialize variables
    latest_file = None
    latest_mtime = None

    # Iterate over files in the folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # Check if it's a file (not a directory)
        if os.path.isfile(file_path):
            # Get the modification time
            mtime = os.path.getmtime(file_path)

            # Compare with the current latest
            if latest_mtime is None or mtime > latest_mtime:
                latest_file = file_path
                latest_mtime = mtime

    return latest_file


def screenshot() -> None:
    img = pyautogui.screenshot()
    filename = generate_random_filename(15, "temp_", ".png")
    img.save(r'Captured_Faces.{}'.format(filename))


def showscreenshot() -> None:
    latest_file = get_latest_file(r'Captured_Faces')
    img = Image.open(latest_file)


def cpu() -> None:
    usage = str(psutil.cpu_percent())
    speak("CPU is at" + usage)

    battery = psutil.sensors_battery()
    speak("battery is at")
    speak(battery.percent)


def joke() -> None:
    for i in range(5):
        speak(pyjokes.get_jokes()[i])


def takeCommand() -> str:
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        r.pause_threshold = 1
        r.energy_threshold = 494
        r.adjust_for_ambient_noise(source, duration=1.5)
        audio = r.listen(source)

    try:
        print('Recognizing..')
        query = r.recognize_google(audio, language='en-in')
        print(f'User said: {query}\n')

    except Exception as e:
        # print(e)
        speak('Say that again please...')
        return 'None'
    return query


def translate(word):
    word = word.lower()
    if word in data:
        speak(data[word])
    elif len(get_close_matches(word, data.keys())) > 0:
        x = get_close_matches(word, data.keys())[0]
        speak('Did you mean ' + x +
              ' instead')
        ans = takeCommand().lower()
        if 'yes' in ans:
            speak(data[x])
        elif 'no' in ans:
            speak("Word doesn't exist. Please make sure you spelled it correctly.")
        else:
            speak("We didn't understand your entry.")

    else:
        speak("Word doesn't exist. Please double check it.")


def get_weather(city):
    api_key = r"your_openweather_api_key"  # Replace with your OpenWeatherMap API key
    base_url = r"https://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "q=" + city + "&appid=" + api_key + "&units=metric"
    response = requests.get(complete_url)
    weather_data = response.json()

    if weather_data["cod"] != "404":
        main = weather_data["main"]
        weather_desc = weather_data["weather"][0]["description"]
        temp = main["temp"]
        return f"{weather_desc} with a temperature of {temp}°C"
    else:
        return "City not found"


def get_definition(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url)
    if response.status_code == 200:
        definition_data = response.json()
        return definition_data[0]["meanings"][0]["definitions"][0]["definition"]
    else:
        return "Definition not found"


def convert_currency(currency_from, currency_to, amount):
    conversion_rates = {
        ("usd", "eur"): 0.85,
        ("eur", "usd"): 1.18,
        ("usd", "lbp"): 89000,
        ("lbp", "usd"): 0.95
    }
    rate = conversion_rates.get((currency_from.lower(), currency_to.lower()))
    if rate:
        converted_amount = float(amount) * rate
        return round(converted_amount, 2)
    else:
        return "Conversion rate not available."



def set_reminder(reminder, reminder_time):
    # Get the current time
    now = datetime.datetime.now()

    if "in" in reminder_time:
        # Parse something like 'in 10 minutes'
        parts = reminder_time.split()
        quantity = int(parts[1])
        unit = parts[2]

        if 'minute' in unit:
            delay = quantity * 60  # minutes to seconds
        elif 'hour' in unit:
            delay = quantity * 3600  # hours to seconds
        elif 'second' in unit:
            delay = quantity  # already in seconds
        else:
            delay = 0
        time.sleep(delay)
        speak(f"Reminder: {reminder}")

    elif "tomorrow" in reminder_time.lower():
        # Parse something like 'tomorrow 8:00 AM'
        tomorrow = now + datetime.timedelta(days=1)
        time_part = reminder_time.split(' ', 1)[1].upper().replace('.', '')  # Normalize time format
        reminder_datetime = datetime.datetime.strptime(time_part, '%I:%M %p')
        reminder_time = reminder_datetime.replace(year=tomorrow.year, month=tomorrow.month, day=tomorrow.day)
        delay = (reminder_time - now).total_seconds()
        time.sleep(delay)
        speak(f"Reminder: {reminder}")

    else:
        # Handle other specific time formats if needed
        reminder_time = reminder_time.upper().replace('.', '')  # Normalize time format
        reminder_datetime = datetime.datetime.strptime(reminder_time, '%I:%M %p')
        delay = (reminder_datetime - now).total_seconds()
        time.sleep(delay)
        speak(f"Reminder: {reminder}")

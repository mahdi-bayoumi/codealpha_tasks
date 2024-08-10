import requests
import json
import pyttsx3
import helperF as helF

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def speak_news():
    url = 'https://newsdata.io/api/1/news?apikey=pub_485924d74583791b7f170a1ff693f7e6d7384&q=lebanon'
    news = requests.get(url).text
    news_dict = json.loads(news)
    arts = news_dict['articles']
    speak('Source: Lebanon News')
    speak('Todays Headlines are..')
    for index, articles in enumerate(arts):
        speak(articles['News'])
        if index == len(arts) - 1:
            break
        speak('Moving on the next news headline, do you want to continue?...')
        ans = helF.takeCommand().lower()
        if 'yes' in ans:
            speak('Sure sir')
        elif 'no' in ans:
            speak('Sure sir')
            break
        else:
            speak('Didnt get that, continue reading ..')
    speak('These were the top headlines, Have a nice day Sir!!..')


def getNewsUrl():
    return 'https://newsdata.io/api/1/news?apikey=pub_485924d74583791b7f170a1ff693f7e6d7384&q=lebanon'


if __name__ == '__main__':
    speak_news()

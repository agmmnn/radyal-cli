import speech_recognition as sr
#https://towardsdatascience.com/building-a-speech-recognizer-in-python-2dad733949b4
my = sr.Recognizer()
audio_file = sr.AudioFile("a.m4a")

with audio_file as s:
    my.adjust_for_ambient_noise(s)
    audio = my.record(s)

result = my.recognize_google(audio)
print(result)

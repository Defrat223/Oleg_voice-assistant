import speech_recognition as sr
import pyttsx3
import subprocess
import webbrowser
import os
import threading
import queue
import time


class VoiceAssistant:
    def __init__(self):
        # Инициализация
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 180)  # Ускоренная речь
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone()
        self.command_queue = queue.Queue()
        self.wake_word = "олег"

        # Оптимизированные настройки микрофона
        with self.mic as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.8)

        # Команды и их обработчики
        self.commands = {
            "калькулятор": self.open_calculator,
            "ютуб": self.open_youtube,
            "вал": self.open_osu,
            "пока": self.shutdown
        }

    def speak(self, text):
        """Быстрое воспроизведение речи"""
        print(f"[Ассистент] {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self, timeout=1.5, phrase_limit=1.2):
        """Оптимизированное прослушивание"""
        try:
            with self.mic as source:
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_limit
                )
            return audio
        except sr.WaitTimeoutError:
            return None

    def open_calculator(self):
        subprocess.Popen("calc.exe")
        self.speak("Открываю калькулятор")

    def open_youtube(self):
        webbrowser.open("https://youtube.com")
        self.speak("Открываю YouTube")
    def open_osu(self):
        # Путь нужно заменить на свой!
        osu_path = r"CD:\Games\Riot Games\Riot Client\RiotClientServices.exe"
        if os.path.exists(osu_path):
            subprocess.Popen(osu_path)
            self.speak("Запускаю валик")
        else:
            self.speak("OSU не найдена")

    def shutdown(self):
        self.speak("До свидания!")
        os._exit(0)

    def wake_detection(self):
        """Сверхбыстрое обнаружение слова 'Олег'"""
        while True:
            audio = self.listen()
            if audio:
                try:
                    text = self.recognizer.recognize_google(audio, language="ru-RU").lower()
                    if self.wake_word in text.split():
                        self.command_queue.put("activated")
                except:
                    pass

    def command_mode(self):
        """Обработка команд"""
        while True:
            if not self.command_queue.empty():
                self.command_queue.get()
                self.speak("Да, слушаю")

                audio = self.listen(timeout=3)
                if audio:
                    try:
                        text = self.recognizer.recognize_google(audio, language="ru-RU").lower()
                        print(f"[Команда] {text}")

                        for cmd in self.commands:
                            if cmd in text:
                                self.commands[cmd]()
                                break
                        else:
                            self.speak("Не понял команды")
                    except:
                        self.speak("Не расслышал")

    def run(self):
        """Запуск ассистента"""
        self.speak(f"Готов к работе. Скажите '{self.wake_word}'")

        # Потоки для параллельной работы
        threading.Thread(target=self.wake_detection, daemon=True).start()
        threading.Thread(target=self.command_mode, daemon=True).start()

        # Основной цикл
        try:
            while True:
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.shutdown()


if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.run()
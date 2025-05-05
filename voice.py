import os
import time
import re
import subprocess
import webbrowser
import threading
import psutil
import pyttsx3
import pyautogui
import speech_recognition as sr
from email.mime.text import MIMEText
import smtplib


# Performance Metrics
total_commands = 0
successful_commands = 0
failed_commands = 0
total_latency = 0.0
metrics_lock = threading.Lock()

def report_metrics():
    global total_commands, successful_commands, failed_commands, total_latency
    with metrics_lock:
        if total_commands == 0:
            print("\n[PERFORMANCE] No commands processed.")
        else:
            accuracy = (successful_commands / total_commands) * 100
            avg_latency = total_latency / total_commands
            print("\n[PERFORMANCE – Last 60s]")
            print(f" Commands processed: {total_commands}")
            print(f" Successful:         {successful_commands}")
            print(f" Failed:             {failed_commands}")
            print(f" Accuracy:           {accuracy:.2f}%")
            print(f" Avg. latency:       {avg_latency:.2f} s")
        total_commands = successful_commands = failed_commands = 0
        total_latency = 0.0
    threading.Timer(60.0, report_metrics).start()

report_metrics()

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen(prompt=None, retries=2):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        if prompt:
            speak(prompt)
        print("Listening...")
        for _ in range(retries):
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=7)
                text = recognizer.recognize_google(audio).lower()
                return text, True
            except sr.WaitTimeoutError:
                print("Timeout. Retrying...")
            except sr.UnknownValueError:
                speak("Could not understand. Try again.")
            except sr.RequestError:
                speak("Speech service error.")
                return None, False
    return None, False

def close_application(app_name):
    closed = False
    for process in psutil.process_iter(['name', 'pid', 'cmdline']):
        try:
            if app_name.lower() in (process.info['name'] or '').lower():
                psutil.Process(process.info['pid']).terminate()
                closed = True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    if closed:
        speak(f"Closed {app_name}")
    else:
        speak(f"{app_name} not running or could not close.")
    return closed

def open_application(app_name):
    app_paths = {
        "notepad": "notepad",
        "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "calculator": "calc",
        "vs code": "code",
    }

    if app_name == "youtube":
        speak("What do you want to search on YouTube?")
        query, ok = listen()
        if not ok or not query:
            speak("Opening YouTube homepage.")
            webbrowser.open("https://www.youtube.com")
            return True

        url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
        webbrowser.open(url)
        speak(f"Searching for {query} on YouTube")
        return True

    elif app_name in app_paths:
        try:
            os.startfile(app_paths[app_name])
            speak(f"Opening {app_name}")
            return True
        except Exception as e:
            speak(f"Could not open {app_name}")
            print(f"Error: {e}")
            return False
    else:
        speak("Application not found.")
        return False
   

def calculate_expression(command):
    match = re.search(r"(\d+)\s*(plus|minus|times|divided by|x|[+\-*/])\s*(\d+)", command)
    if not match:
        speak("Couldn't understand the calculation.")
        return False
    num1, op, num2 = match.groups()
    num1, num2 = float(num1), float(num2)
    result = None
    if op in ("plus", "+"): result = num1 + num2
    elif op in ("minus", "-"): result = num1 - num2
    elif op in ("times", "x", "*"): result = num1 * num2
    elif op in ("divided by", "/"):
        if num2 == 0:
            speak("Division by zero.")
            return False
        result = num1 / num2
    else:
        speak("Unknown operator.")
        return False
    speak(f"The result is {result}")
    subprocess.Popen("calc.exe")
    time.sleep(2)
    pyautogui.write(f"{num1}{op}{num2}", interval=0.2)
    pyautogui.press("enter")
    return True

def send_email():
    sender_email = "bugadeprajakta26@gmail.com"
    sender_password = "nsaj nlrk yogx evrh"

    contacts = {
        "riddhi gori": "riddhi.dg@somaiya.edu",
        "sejal kamaliya": "sejal.kamaliya@somaiya.edu",
        "aastha bhatt": "aasttha.bhatt@somaiya.edu",
        "rishi": "h.nirale@somaiya.edu",
    }

    to_name, ok = listen("Who do you want to email?")
    if not ok or not to_name:
        return False
    to_email = contacts.get(to_name, to_name)
    subject, ok = listen("What is the subject?")
    if not ok or not subject:
        return False
    message, ok = listen("What should I say?")
    if not ok or not message:
        return False

    try:
        msg = MIMEText(message)
        msg['From'] = sender_email
        msg['To'] = to_email
        msg['Subject'] = subject

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, msg.as_string())
        server.quit()
        speak("Email sent.")
        return True
    except Exception as e:
        speak("Failed to send email.")
        print(e)
        return False

def track_metrics(success, latency):
    global total_commands, successful_commands, failed_commands, total_latency
    with metrics_lock:
        total_commands += 1
        total_latency += latency
        if success:
            successful_commands += 1
        else:
            failed_commands += 1

def main():
    speak("Voice system ready. Say your command.")
    while True:
        start_time = time.time()
        command, ok = listen()
        if not ok or not command:
            track_metrics(False, time.time() - start_time)
            continue

        command = command.lower()
        result = False
        if command.startswith("open "):
            app = command.replace("open ", "").strip()
            result = open_application(app)
        elif command.startswith("close "):
            app = command.replace("close ", "").strip()
            if app == "youtube":
                for proc in psutil.process_iter(['name', 'cmdline']):
                    try:
                        if "chrome.exe" in (proc.info['name'] or "") and any("youtube.com" in part for part in proc.info['cmdline']):
                            proc.terminate()
                            result = True
                    except Exception:
                        pass
                speak("Closed YouTube" if result else "YouTube not running")
            else:
                result = close_application(app)
        elif "calculate" in command or any(op in command for op in ("plus", "minus", "times", "divided by")):
            result = calculate_expression(command)
        elif "send email" in command:
            result = send_email()
        elif "search" in command:
            query, ok = listen("What do you want to search?")
            if ok:
                webbrowser.open(f"https://www.google.com/search?q={query}")
                speak(f"Searching {query}")
                result = True
        elif command in ("exit", "stop", "quit"):
            speak("Goodbye!")
            break
        else:
            speak("Command not recognized.")

        latency = time.time() - start_time
        track_metrics(result, latency)

if __name__ == "__main__":
    main()

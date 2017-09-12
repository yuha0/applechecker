import smtplib
from email.mime.text import MIMEText
from socket import gaierror


class BaseAlert(object):
    def _print_ahead(self, method):
        def wrapper(msgbody):
            print(msgbody)
            method(msgbody)
        return wrapper


class SmtpAlert(BaseAlert):
    def __init__(self, dest=None, login=None, password=None):
        self.dest = dest
        self.login = login
        self.password = password
        self.send = self._print_ahead(self.send_smtp)

    def send_smtp(self, msgbody):
        message = MIMEText(msgbody, _charset="UTF-8")
        message['From'] = self.login
        message['To'] = self.dest
        message['Subject'] = "Apple Stock Alert"

        try:
            mailer = smtplib.SMTP('smtp.gmail.com:587')
        except gaierror:
            print("Couldn't reach Gmail server")
            return
        mailer.ehlo()
        mailer.starttls()
        mailer.ehlo()
        mailer.login(self.login, self.password)
        mailer.sendmail(self.login, self.dest, message.as_string())
        mailer.close()

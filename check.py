#!/usr/bin/env python
from __future__ import print_function
import sys
import time
import json
import smtplib
from email.mime.text import MIMEText
from socket import gaierror
try:
    # python 3
    from urllib.request import urlopen
    from urllib.parse import urlencode
except ImportError:
    # python2
    from urllib import urlopen
    from urllib import urlencode


# only tested for US stores and US text message
URL = "http://www.apple.com/shop/retail/pickup-message"
BUY = "http://store.apple.com/xc/product/"

DATEFMT = "[%m/%d/%Y-%H:%M:%S]"
LOADING = ['-', '\\', '|', '/']


class Alert(object):
    def __init__(self, dest=None, login=None, credential=None):
        if not dest:
            self.send = lambda x: None
            return
        self.dest = dest
        self.login = login
        self.password = credential
        self.send = self._print_ahead(self.send_smtp)

    def _print_ahead(self, method):
        def wrapper(msgbody):
            print(msgbody)
            method(msgbody)
        return wrapper

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


def main(model, zipcode, sec=5, dest=None, login=None, pwd=None,):
    good_stores = []
    my_alert = Alert(dest, login, pwd)
    initmsg = ("{0} Start tracking {1} in {2}. "
               "Alert will be sent to {3}").format(time.strftime(DATEFMT),
                                                   model, zipcode, dest)
    my_alert.send(initmsg)
    params = {'parts.0': model,
              'location': zipcode}
    sec = int(sec)
    i, cnt = 0, sec
    while True:
        if cnt < sec:
            # loading sign refreashes every second
            print('Checking...{}'.format(LOADING[i]), end='\r')
            sys.stdout.flush()
            i = i + 1 if i < 3 else 0
            cnt += 1
            time.sleep(1)
            continue
        cnt = 0

        try:
            response = urlopen(
                "{}?{}".format(URL, urlencode(params)))
            stores = json.load(response)['body']['stores'][:8]
        except (ValueError, KeyError, gaierror) as reqe:
            print("Failed to query Apple Store, details: {}".format(reqe))
            time.sleep(int(sec))
            continue

        for store in stores:
            sname = store['storeName']
            item = store['partsAvailability'][model]['storePickupProductTitle']
            if store['partsAvailability'][model]['pickupDisplay'] \
                    == "available":
                if sname not in good_stores:
                    good_stores.append(sname)
                    msg = u"{} Found it! {} has {}! {}{}".format(
                        time.strftime(DATEFMT), sname, item, BUY, model)
                    my_alert.send(msg)
            else:
                if sname in good_stores:
                    good_stores.remove(sname)
                    msg = u"{} Oops all {} in {} are gone :( ".format(
                        time.strftime(DATEFMT), item, sname)
                    my_alert.send(msg)

        if good_stores:
            print(u"{current} Still Avaiable: {stores}".format(
                current=time.strftime(DATEFMT),
                stores=', '.join([s for s in good_stores])
                if good_stores else "None"))


if __name__ == '__main__':
    main(*sys.argv[1:])

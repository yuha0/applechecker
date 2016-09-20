#!/usr/bin/env python
import time
import sys
import smtplib
from socket import gaierror
import requests

# only tested for US stores and US text message
URL = "http://www.apple.com/shop/retail/pickup-message"
BUY = "http://store.apple.com/xc/product/"
SMS = "http://textbelt.com/text"

def check_stock(model, zipcode, dest, sec=5, login=None, pwd=None):
    good_stores = []
    my_alert = Alert(dest, login, pwd)
    initmsg = "{0} start tracking {1} in {2}. Alert will sent to {3}".format(
        time.strftime("%m/%d/%Y %H:%M:%S"), model, zipcode, dest)
    print initmsg
    my_alert.send(initmsg)
    params = {'parts.0': model,
              'location': zipcode}

    while True:
        time.sleep(int(sec))
        if good_stores:
            print "=================================="
            print "[{current}] Avaiable: {stores}".format(
                current=time.strftime("%m/%d/%Y %H:%M:%S"),
                stores=', '.join([s.encode('utf-8') for s in good_stores])
                        if good_stores else "None")

        try:
            stores = requests.get(URL, params=params) \
                    .json()['body']['stores'][:8]
        except (ValueError, KeyError, gaierror):
            print "Bad response from server..."
            continue
        for store in stores:
            sname = store['storeName']
            item = store['partsAvailability'][model]['storePickupProductTitle']
            if store['partsAvailability'][model]['pickupDisplay'] \
                        == "available":
                if sname not in good_stores:
                    good_stores.append(sname)
                    msg = "Go!! {store} has {item}!! {buy}{model}".format(
                        store=sname, item=item, buy=BUY, model=model)
                    print "{0} {1}".format(time.strftime("%m/%d/%Y %H:%M:%S"),
                                           msg)
                    my_alert.send(msg)
            else:
                if sname in good_stores:
                    good_stores.remove(sname)
                msg = "Oops all {item} in {store} are gone :( ".format(
                    item=item, store=sname)
                print "{0} {1}".format(time.strftime("%m/%d/%Y %H:%M:%S"),
                                       msg)

class Alert(object):
    def __init__(self, dest, login=None, password=None):
        self.dest = dest
        if login and password:
            self.login = login
            self.password = password
            self.send = self.send_email
        else:
            self.send = self.send_sms

    def send_email(self, msgbody):
        message = "From: {0}\nTo: {1}\nSubject: {2}\n\n{3}".format(
            self.login, self.dest, "Apple Stock Alert", msgbody)
        try:
            mailer = smtplib.SMTP('smtp.gmail.com:587')
        except gaierror:
            print "Couldn't reach Gmail server"
            return
        mailer.ehlo()
        mailer.starttls()
        mailer.ehlo()
        mailer.login(self.login, self.password)
        mailer.sendmail(self.login, self.dest, message)
        mailer.close()

    def send_sms(self, message):
        try:
            response = requests.post(SMS, data={
                'number': self.dest, 'message': message}).json()
            if response['success'] is not True:
                print response['message']
                sys.exit(2)
        except gaierror:
            print "Couldn't reach TextBelt"
        if response.json()['success'] is not True:
            print "Failed to send SMS"
            sys.exit(2)

if __name__ == '__main__':
    check_stock(*sys.argv[1:])

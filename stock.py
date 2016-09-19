#!/usr/bin/env python
import time
import sys
import smtplib
import requests

URL = "http://www.apple.com/shop/retail/pickup-message"
BUY = "http://store.apple.com/xc/product/"

def check_stock(model, zip_, dest, sec=5, login=None, pwd=None):
    good_stores = []
    my_alert = Alert(dest, login, pwd)
    initmsg = "{0} start tracking {1} in {2}. Alert will sent to {3}".format(
        time.strftime("%m/%d/%Y %H:%M:%S"), model, zip_, dest)
    print initmsg
    my_alert.send(initmsg)
    params = {'parts.0': model,
              'location': zip_}

    while True:
        print "=================================="
        print "[{current}] Avaiable: {stores}".format(
            current=time.strftime("%m/%d/%Y %H:%M:%S"),
            stores=', '.join([store.encode('utf-8') for store in good_stores])
                    if good_stores else "None")

        try:
            stores = requests.get(URL, params=params).json()['body']['stores'][:8]
        except (ValueError, KeyError):
            print "Bad response from server..."
            continue
        for store in stores:
            sname = store['storeName']
            item = store['partsAvailability'][model]['storePickupProductTitle']
            if store['partsAvailability'][model]['pickupDisplay'] \
                        == "available":
                if sname not in good_stores:
                    good_stores.append(sname)
                    msg = "Gooo!! {store} has {item}!! {buy}{model}".format(
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
                    my_alert.send(msg)
        time.sleep(int(sec))

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
        mailer = smtplib.SMTP('smtp.gmail.com:587')
        mailer.ehlo()
        mailer.starttls()
        mailer.ehlo()
        mailer.login(self.login, self.password)
        mailer.sendmail(self.login, self.dest, message)
        mailer.close()

    def send_sms(self, message):
        r = requests.post('http://textbelt.com/text', data={
            'number': self.dest, 'message': message})

if __name__ == '__main__':
    check_stock(*sys.argv[1:])

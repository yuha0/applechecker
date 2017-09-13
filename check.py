#!/usr/bin/env python
from __future__ import print_function
import sys
import time
import json
from socket import gaierror
try:
    # python 3
    from urllib.request import urlopen
    from urllib.parse import urlencode
except ImportError:
    # python2
    from urllib import urlopen
    from urllib import urlencode
from Alert import SmtpAlert

# only tested for US stores
URL = "http://www.apple.com/shop/retail/pickup-message"
BUY = "http://store.apple.com/xc/product/"

DATEFMT = "[%m/%d/%Y-%H:%M:%S]"
LOADING = ['-', '\\', '|', '/']

INPUT_ERRORS = {"Products Invalid or not buyable",
                "Invalid zip code or city/state."}

INITMSG = "{} Start monitoring {} inventory in area {}."


def main(model, zipcode, sec=5, *alert_params):
    good_stores = []
    my_alert = SmtpAlert(*alert_params)
    params = {'parts.0': model,
              'location': zipcode}
    sec = int(sec)
    i, cnt = 0, sec
    init = True
    while True:
        if cnt < sec:
            # loading sign refreshes every second
            print('Checking...{}'.format(LOADING[i]), end='\r')
            i = i + 1 if i < 3 else 0
            cnt += 1
            time.sleep(1)
            continue
        cnt = 0
        try:
            response = urlopen(
                "{}?{}".format(URL, urlencode(params)))
            json_body = json.load(response)['body']
            stores = json_body['stores'][:8]
            item = (stores[0]['partsAvailability']
                    [model]['storePickupProductTitle'])
            if init:
                my_alert.send(INITMSG.format(
                    time.strftime(DATEFMT), item, zipcode))
                init = False
        except (ValueError, KeyError, gaierror) as reqe:
            error_msg = "Failed to query Apple Store, details: {}".format(reqe)
            try:
                error_msg = json_body['errorMessage']
                if error_msg in INPUT_ERRORS:
                    sys.exit(1)
            except KeyError:
                pass
            finally:
                print(error_msg)
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

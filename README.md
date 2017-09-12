# applechecker

> Check Apple Store Inventory

Keep checking Apple Store inventory and send you alert when nearby stores have your desired device in stock.
Also let you know if inventory becomes zero again so you don't jump out of bed when it is already too late.

* [Prerequisites](#prerequisites)
* [Usage](#usage)

## Prerequisites

* A gmail account if want email alert. (Got refused by Gmail because the app is insecure? [Enable 2-Step Verification](https://support.google.com/accounts/answer/185839?hl=en) and [generate an App password]() for it. Or follow [this instruction](https://support.google.com/accounts/answer/6010255?hl=en) to allow insecure login)

## Usage

```
python check.py <model> <zipcode> <check interval in seconds> <emails or phone numbers delimited by comma> <your gmail account if you want email alerts> <your gmail password if you want email alerts>
```

### Example:

Every 5 seconds, check availability of `Apple Watch Stainless Steel Case with White Sport Band` near zipcode 12345 and send email alert to `recipient@example.com` using gmail account `sender@gmail.com`.

```
python /path/to/check.py "MNPR2LL/A" "12345" 5 recipient@example.com sender@gmail.com sender_password
```

Model number is a unique identifier, U.S. models end with "LL/*". (https://www.theiphonewiki.com/wiki/Model_Regions)

* For Apple Watch: model number hides in query string in URL of the item page.

    Example:
    `http://www.apple.com/shop/buy-watch/apple-watch/silver-stainless-steel-stainless-steel-sport-band?preSelect=true&product=`**`MNPR2LL/A`**`&step=detail#`

* iPhone: inspect the item page and look for a request to `http://www.apple.com/shop/delivery-message?`

    Example:
    `http://www.apple.com/shop/delivery-message?parts.0=`**`MN5L2LL%2FA`**`&cppart=TMOBILE%2FUS&_=1474171709609`

    or just check your model number here: http://www.everyi.com/

To verify, visit `http://store.apple.com/xc/product/<model numer>` and see if it shows the product you want.

### Docker Example:

```
# foreground
docker run --rm -t yuha0/applechecker "MNPR2LL/A" "12345"  5 recipient@example.com sender@gmail.com "ekffyblvhbyhpowd"
```

```
# background
docker run -d --restart always yuha0/applechecker "MNPR2LL/A" "12345" 5 recipient@example.com sender@gmail.com "ekffyblvhbyhpowd"
```

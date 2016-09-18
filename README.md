# applechecker

> Check Apple Store Inventory

Keep checking Apple Store inventory and send you alert when nearby store have your desired device in stock.
Also let you know if inventory becomes zero again so you don't jump out of bed when it is already too late.

* [Prerequisites](#prerequisites)
* [Usage](#usage)

## Prerequisites

* `pip install requests`

* A gmail account if want email alert.

* For SMS alert, the script uses the free service provided by [TextBelt](http://textbelt.com/), which has some limitations like "IP addresses are limited to 75 texts per day" and "Phone numbers are limited to 3 texts every 3 minutes". Check their page for details.

## Usage

```
python stock.py <model> <zipcode> <emails or phone numbers delimited by comma> <check interval in seconds> <your gmail account if you want email alerts> <your gmail password if you want email alerts>
```

###Example:

Every 5 seconds, check availability of `Apple Watch Stainless Steel Case with White Sport Band` near zipcode 22102 and send email alert to `recipient@example.com` using gmail account `sender@gmail.com`.

```
python /path/to/stock.py "MNPR2LL/A" "22102" "recipient@example.com" 5 sender@gmail.com sender_password
```

Every 10 seconds, check availability of `iPhone 7 Plus T-Mobile Jet Black 128GB` near zipcode 22102 and send sms alert to `2021234567`.

```
python /path/to/stock.py "MN5L2LL/A" "22102" "2021234567" 10
```

Model number is a unique identifier, U.S. models end with "LL/*". (https://www.theiphonewiki.com/wiki/Model_Regions)

To find out the model number for a specific product:

* Apple Watch: model number hides in query string in URL of the item page.

    Example:
    `http://www.apple.com/shop/buy-watch/apple-watch/silver-stainless-steel-stainless-steel-sport-band?preSelect=true&product=`**`MNPR2LL/A`**`&step=detail#`

* iPhone: inspect the item page and look for a request to `http://www.apple.com/shop/delivery-message?`

    Example:
    `http://www.apple.com/shop/delivery-message?parts.0=`**`MN5L2LL%2FA`**`&cppart=TMOBILE%2FUS&_=1474171709609`

For a complete list: http://www.everyi.com/



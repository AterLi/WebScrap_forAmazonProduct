from bs4 import BeautifulSoup
import requests
import lxml
import os
import sendgrid
from sendgrid.helpers.mail import *
from twilio.rest import Client

api_key = os.environ.get("API_KEY_ENV")
acc_sid = os.environ.get("ACH_SID")
auth_token = os.environ.get("AUTH_TOKEN")
twilio_nr = os.environ.get("TWILIO_NR")
your_nr = os.environ.get("YOUR_NR")


url = "https://www.amazon.com/dp/B075CYMYK6?ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6&th=1"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

web_data = requests.get(url=url, headers=headers)
data = web_data.text


soup = BeautifulSoup(data, "lxml")
# print(soup.prettify())
title = soup.find("span", id="productTitle").getText().split()[0]
price = float(soup.find("span", class_="a-offscreen").getText().split("$")[1])
# print(price)
change_title = title + soup.find("span", id="productTitle").getText().split()[1]
# print(change_title)

if price < 99:
    print(price)
# Send sms
    client = Client(acc_sid, auth_token)
    message = client.messages.create(
        body=f"Subject: Convenable price\n Your selected product ({change_title}) now costs ({price}),"
             f" is up to you to decide buying this",
        from_= twilio_nr,
        to= your_nr)


# Send mail using twilio
#     sg = sendgrid.SendGridAPIClient(api_key=api_key)
#     from_email = Email("mail")
#     to_email = To("mail")
#     subject = "Coninient price!"
#     content = Content("text/plain",
#                       f"Your selected product now costs ({price}), is up to you to decide buying this")
#     mail = Mail(from_email, to_email, subject, content)
#     resource = sg.client.mail.send.post(request_body=mail.get())
#     print(response.status_code)
#     print(response.body)
#     print(response.headers)
import yagmail
import os

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_TO = os.getenv("EMAIL_TO")

def send_alert(item_name, current_price, alert_price):
    yag = yagmail.SMTP(EMAIL_USER, EMAIL_PASS)
    subject = f"Price Alert: {item_name} is now ${current_price}"
    contents = f"{item_name} dropped below ${alert_price}! Current price: ${current_price}"
    yag.send(EMAIL_TO, subject, contents)
    print(f"Alert sent for {item_name}")
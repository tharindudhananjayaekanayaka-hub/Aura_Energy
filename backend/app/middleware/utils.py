import os
import random
from twilio.rest import Client
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

load_dotenv()

# 1. OTP එකක් හදන function එක
def generate_otp():
    return str(random.randint(100000, 999999))

# 2. SMS එකක් යවන function එක (Twilio)
def send_otp_sms(phone_number, otp_code):
    try:
        client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
        message = client.messages.create(
            body=f"Your AuraEnergy Verification Code is: {otp_code}",
            from_=os.getenv("TWILIO_PHONE_NUMBER"),
            to=phone_number
        )
        return message.sid
    except Exception as e:
        print(f"Twilio Error: {e}")
        return None

# 3. Welcome Email එකක් යවන function එක (SendGrid)
def send_welcome_email(user_email, username):
    try:
        message = Mail(
            from_email=os.getenv("FROM_EMAIL"),
            to_emails=user_email,
            subject='Welcome to AuraEnergy AI!',
            html_content=f'''
                <div style="font-family: Arial, sans-serif; padding: 20px; border: 1px solid #eee;">
                    <h2 style="color: #2e7d32;">Welcome to AuraEnergy AI, {username}!</h2>
                    <p>ඔබගේ ගිණුම සාර්ථකව නිර්මාණය කර ඇත. දැන් ඔබට බලශක්ති පරිභෝජනය බුද්ධිමත්ව කළමනාකරණය කළ හැකිය.</p>
                    <p style="color: #666;">Best Regards,<br>AuraEnergy Support Team</p>
                </div>
            '''
        )
        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        sg.send(message)
    except Exception as e:
        print(f"SendGrid Error: {e}")
from decouple import config
import smtplib

try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('recarnationtechtitans@gmail.com', config('EMAIL_HOST_PASSWORD'))
    print("Logged in successfully!")
    server.quit()
except Exception as e:
    print(f"Error: {e}")

import requests
from bs4 import BeautifulSoup
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

# Email configuration for Seznam.cz
sender_email = "kaktusnotifikace@seznam.cz"
receiver_email = "hosekvitek@gmail.com"
smtp_server = "smtp.seznam.cz"
smtp_port = 465
smtp_username = "kaktusnotifikace@seznam.cz"
smtp_password = "kaktusmail"

# URL of the newsletter page
url = "https://www.mujkaktus.cz/novinky"

# Global dictionary to store the last email info
last_email_info = {"subject": "", "body": ""}

# Function to save email content to the cache
def save_email_info(subject, body):
    global last_email_info # Use the global keyword to access the global dictionary
    last_email_info["subject"] = subject # Update the subject value
    last_email_info["body"] = body # Update the body value

# Function to read email info from the cache
def read_email_info():
    global last_email_info # Use the global keyword to access the global dictionary
    subject = last_email_info["subject"] # Get the subject value
    body = last_email_info["body"] # Get the body value
    return subject, body

# Function to check for new posts and send an email if needed
def check_new_posts():
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    latest_post = soup.find("div", class_="article")
    if latest_post is not None:
        post_title = latest_post.find("h3").get_text(strip=True)
        post_content = latest_post.find("p").get_text(strip=True)
        subject = f"Kaktus - {post_title}" # Changed the subject to include the post title instead of the date
        body = f"Title: {post_title}\nContent: {post_content}"

        last_subject, last_body = read_email_info()

        # Check if the same email body has already been sent today
        if body != last_body:
            # Check if the current time is between 8 AM and 6 PM
            current_hour = datetime.now().hour
            if 6 <= current_hour < 22:
                send_email(subject, body)
                save_email_info(subject, body)
            else:
                print("Current time is not within the specified range.")
        else:
            print("Email body is the same as the last one.")

    else:
        print("No post found.")

# Function to send an email
def send_email(subject, body):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print("Failed to send email:", e)

while True: # Added a while loop to run the check_new_posts function continuously with a delay of 10 seconds
    check_new_posts()
    time.sleep(10)

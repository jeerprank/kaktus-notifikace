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

# Mapping of month numbers to month names
month_names = {
    "1": "January",
    "2": "February",
    "3": "March",
    "4": "April",
    "5": "May",
    "6": "June",
    "7": "July",
    "8": "August",
    "9": "September",
    "10": "October",
    "11": "November",
    "12": "December"
}

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

# Function to save timestamp and email content to a file
def save_email_info(timestamp, subject, body):
    with open("last_email_info.txt", "w", encoding="utf-8") as file:
        file.write(f"{timestamp}\n{subject}\n{body}")

# Function to read email info from the file
def read_email_info():
    try:
        with open("last_email_info.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()
            if len(lines) >= 3:
                timestamp = float(lines[0])
                subject = lines[1].strip()
                body = lines[2].strip()
                return timestamp, subject, body
            else:
                return 0, "", ""
    except FileNotFoundError:
        return 0, "", ""

# Function to check for new posts
def check_new_posts():
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    latest_post = soup.find("div", class_="article")
    if latest_post is not None:
        post_title = latest_post.find("h3").get_text(strip=True)
        post_content = latest_post.find("p").get_text(strip=True)

        formatted_date = datetime.now().strftime("%d.%m")

        subject = f"Kaktus - {formatted_date}"
        body = f"Title: {post_title}\nContent: {post_content}"

        current_time = time.time()
        last_email_time, last_subject, last_body = read_email_info()

        if current_time - last_email_time >= 3600 and (subject != last_subject or body != last_body):
            send_email(subject, body)
            save_email_info(current_time, subject, body)
        else:
            print("An hour has not passed since the last email, or the same email has already been sent.")
    else:
        print("No post found.")

while True:
    check_new_posts()
    time.sleep(300)

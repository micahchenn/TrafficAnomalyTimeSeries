import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import pandas as pd
from datetime import datetime

def send_email(subject, body, to_emails, attachment_path=None):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_user = 'micahchen40@gmail.com'
    smtp_password = 'tfja evae zpbw lmpl'  # Replace with your actual app-specific password

    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = ', '.join(to_emails)
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    if attachment_path and os.path.exists(attachment_path):
        with open(attachment_path, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(attachment_path)}")
            msg.attach(part)

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_user, to_emails, msg.as_string())
        server.quit()
        print(f"Email sent successfully to {to_emails}")
    except Exception as e:
        print(f"Failed to send email: {e}")

def check_and_send_anomalies():
    summary_path = 'summary_of_anomalies.csv'
    to_emails = ['sarahpalmer127@gmail.com']

    # Check if the summary file exists
    if not os.path.exists(summary_path):
        subject = "Summary File Missing"
        body = "The summary of anomalies file is missing."
        send_email(subject, body, to_emails)
        return

    try:
        # Load the summary CSV file
        summary_df = pd.read_csv(summary_path)

        # Check if the file contains the necessary columns
        if 'has_anomalies' not in summary_df.columns:
            subject = "Invalid Summary File"
            body = "The summary of anomalies file does not contain the required 'has_anomalies' column."
            send_email(subject, body, to_emails)
            return

        # Check for anomalies
        if not summary_df.empty and summary_df['has_anomalies'].any():
            num_anomalies = summary_df['has_anomalies'].sum()
            subject = "*Anomalies Detected*"
            body = (f"Total anomalies detected: {num_anomalies}\n"
                    "Please find attached the summary of anomalies.")
            send_email(subject, body, to_emails, attachment_path=summary_path)
        else:
            subject = "No Anomalies Detected"
            body = "No anomalies were detected in the data."
            send_email(subject, body, to_emails)

    except Exception as e:
        subject = "Error Processing Summary File"
        body = f"An error occurred while processing the summary file: {e}"
        send_email(subject, body, to_emails)

# Automatically send the email after checking for anomalies
check_and_send_anomalies()

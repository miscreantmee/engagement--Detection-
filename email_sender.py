import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('email.html')

@app.route('/send_email', methods=['POST'])
def send_email():
    if request.method == 'POST':
        # Replace with a list of recipient email addresses
        recipient_emails = ['jainnancy779@gmail.com','thakurhemant044@gmail.com','kashyapprabhat254@gmail.com']
        
        sender_email = 'rishichabbra149@gmail.com'  # Replace with your Gmail address
        sender_password = 'nlpy qmbm eode cfrl'  # Use your App Password here

        subject = 'Hello from Student Engagement Detection in E-learning  Environments!'
        message = """Warning!,Pay Attention Use a Timer:
Practice the Pomodoro Technique—work for 25 minutes, then take a 5-minute break. Repeat this cycle to maintain focus and productivity.

Stay Organized:
Use planners or apps to organize your tasks and schedule. Having a structured plan helps reduce anxiety and keeps you on track.

Prioritize Tasks:
Start with the most challenging tasks when your energy and focus are high. As you complete tasks, you'll gain momentum.

Stay Hydrated and Eat Well:
Drink enough water and maintain a balanced diet. Dehydration and hunger can affect concentration."""

        try:
            # Create a multipart message
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['Subject'] = subject

            # Attach the message body
            msg.attach(MIMEText(message, 'plain'))

            # Attach a media file (e.g., a PDF)
            file_path = 'D:/STARTUP1/Mentor/EmotionRecognition.png'  # Replace with the actual file path
            attachment = open(file_path, 'rb')

            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={file_path}')

            msg.attach(part)

            # Connect to Gmail's SMTP server
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)

            for recipient_email in recipient_emails:
                # Set the recipient for this iteration
                msg['To'] = recipient_email

                # Send the email to the current recipient
                server.sendmail(sender_email, recipient_email, msg.as_string())

            server.quit()

            return 'Email sent successfully!'
        except Exception as e:
            return f'Email could not be sent. Error: {str(e)}'

if __name__ == '__main__':
    app.run(debug=True)

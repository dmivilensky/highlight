import configparser
import smtplib
import sys
import os
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email_named(to_addr, file_path, file_name):
    config = configparser.ConfigParser()
    config.read(os.path.realpath(__file__)[:-17] + "/mail.ini")
    send_email('HighLight: документ ' + file_name, to_addr, config["Credentials"]["user"], 'Документ прислан сайтом highlight.spb.ru', config["Credentials"]["user"], config["Credentials"]["pwd"], file_path, file_name)


def send_email(subject, to_addr, from_addr, body_text, uname, pswd, file_path, file_name):
    """
    Send an email
    """

    msg = MIMEMultipart()
    msg["From"] = from_addr
    msg["Subject"] = subject
    header = 'Content-Disposition', 'attachment; filename="%s"' % file_name

    if body_text:
        msg.attach(MIMEText(body_text))

    msg["To"] = to_addr
    attachment = MIMEBase('application', "octet-stream")

    try:
        with open(file_path, "rb") as fh:
            data = fh.read()

        attachment.set_payload(data)
        encoders.encode_base64(attachment)
        attachment.add_header(*header)
        msg.attach(attachment)
    except IOError:
        msg = "Error opening attachment file %s" % file_path
        print(msg)
        sys.exit(1)

    server = smtplib.SMTP(host='smtp.gmail.com', port=587)
    server.starttls()
    server.login(uname, pswd)
    server.sendmail(from_addr, [to_addr], msg)
    server.quit()


if __name__ == "__main__":
    send_email_named("sss", "sss", "ddd")
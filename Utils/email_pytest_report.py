import smtplib
import os, sys
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import mimetypes
from email import encoders
from os.path import dirname

import Data.email_conf as conf_file

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class Email_Pytest_Report:
    def __init__(self):
        self.smtp_ssl_host = conf_file.smtp_ssl_host
        self.smtp_ssl_port = conf_file.smtp_ssl_port
        self.username = conf_file.username
        self.password = conf_file.app_password
        self.sender = conf_file.sender
        self.targets = conf_file.targets

    def get_test_report_data(self, html_body_flag=True, report_file_path='default'):
        "get test report data from pytest_report.html or pytest_report.txt or from user provided file"
        if html_body_flag == True and report_file_path == 'default':
            test_report_file = os.path.abspath(os.path.join(os.path.dirname(__file__), 'report.html'))
            print('get_test_report_data::test_report_file:', test_report_file)

        elif html_body_flag == False and report_file_path == 'default':
            test_report_file = os.path.abspath(os.path.join(os.path.dirname(__file__), 'report.log'))
        else:
            test_report_file = report_file_path
        if not os.path.exists(test_report_file):
            raise Exception("File '%s' does not exist. Please provide valid file" % test_report_file)

        with open(test_report_file, "r") as in_file:
            testdata = ""
            for line in in_file:
                testdata = testdata + '\n' + line
        return testdata

    def get_attachment(self, attachment_file_path='default'):
        "Get attachment and attach it to mail"
        if attachment_file_path == 'default':
            attachment_report_file = os.path.abspath(os.path.join(dirname(dirname(__file__)), 'pytest_report.html'))
        else:
            attachment_report_file = attachment_file_path
        if not os.path.exists(attachment_report_file):
            raise Exception("File '%s' does not exist. Please provide valid file" % attachment_report_file)

        ctype, encoding = mimetypes.guess_type(attachment_report_file)
        if ctype is None or encoding is not None:
            ctype = 'application/octet-stream'
        maintype, subtype = ctype.split('/', 1)
        if maintype == 'text':
            fp = open(attachment_report_file)
            attachment = MIMEText(fp.read(), subtype)
            fp.close()
        elif maintype == 'image':
            fp = open(attachment_report_file, 'rb')
            attachment = MIMEImage(fp.read(), subtype)
            fp.close()
        elif maintype == 'audio':
            fp = open(attachment_report_file, 'rb')
            attachment = MIMEAudio(fp.read(), subtype)
            fp.close()
        else:
            fp = open(attachment_report_file, 'rb')
            attachment = MIMEBase(maintype, subtype)
            attachment.set_payload(fp.read())
            fp.close()
            encoders.encode_base64(attachment)
        attachment.add_header('Content-Disposition',
                              'attachment',
                              filename=os.path.basename(attachment_report_file))
        return attachment

    def send_test_report_email(self, html_body_flag=True, attachment_flag=False, report_file_path='default'):
        if html_body_flag == True and attachment_flag == False:
            testdata = self.get_test_report_data(html_body_flag,
                                                 report_file_path)
            message = MIMEText(testdata, "html")
        elif html_body_flag == False and attachment_flag == False:
            testdata = self.get_test_report_data(html_body_flag,
                                                 report_file_path)
            message = MIMEText(testdata)
        elif html_body_flag == True and attachment_flag == True:
            message = MIMEMultipart()
            html_body = MIMEText('''<p>Hello,</p>
                                     <p>&nbsp; &nbsp; &nbsp; &nbsp; Please check the attachment to see test built report.</p>
                                     <p><strong>Note: For best UI experience, download the attachment and open using Chrome browser.</strong></p>
                                 ''', "html")
            message.attach(html_body)
            attachment = self.get_attachment(report_file_path)
            message.attach(attachment)
        else:
            message = MIMEMultipart()
            plain_text_body = MIMEText('''Hello,\n\tPlease check attachment to see test built report.
                                       \n\nNote: For best UI experience, download the attachment and open  using Chrome browser.''')  # Add/Update email body message here as per your requirement
            message.attach(plain_text_body)
            attachment = self.get_attachment(report_file_path)
            message.attach(attachment)

        message['From'] = self.sender
        message['To'] = ', '.join(self.targets)
        message['Subject'] = 'Synup Automation Script generated test report'  # Update email subject here
        # Send Email
        server = smtplib.SMTP_SSL(self.smtp_ssl_host, self.smtp_ssl_port)
        server.login(self.username, self.password)
        server.sendmail(self.sender, self.targets, message.as_string())
        server.quit()
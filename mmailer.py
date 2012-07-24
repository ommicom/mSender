__author__ = 'Omic'

import smtplib

from email import encoders
from email.mime.text import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase

class mMailer():
    smtpServer = None
    smtpPort = None
    smtpUser = None
    smtpPasswd = None
    fromAddr = None
    auth = False
    tls = False
    logger = None
    SMTP = None
    msg = None

    def __init__(self, smtpServer, smtpPort=25, smtpUser=None, smtpPasswd=None, fromaddr=None, auth=False, tls=False, logger=None):
        self.smtpServer = smtpServer
        self.smtpPort = smtpPort
        self.smtpUser = smtpUser
        self.smtpPasswd = smtpPasswd
        self.fromAddr = fromaddr
        self.auth = auth
        self.tls = tls
        self.logger = logger

    def checkAvailabilityServer(self):
        try:
            self.SMTP = smtplib.SMTP()
            self.SMTP.connect(self.smtpServer, self.smtpPort)
            resHelo=self.SMTP.ehlo()
            if self.tls:
                self.SMTP.starttls()
            if self.auth:
                self.SMTP.login(self.smtpUser, self.smtpPasswd)
        except smtplib.SMTPConnectError as err:
            if self.logger: self.logger.debug('SMTP server connection error {0}:{1}'.format(type(err), err))
        except smtplib.SMTPAuthenticationError as err:
            if self.logger: self.logger.debug('Authentication error {0}:{1}'.format(type(err), err))
        except smtplib.SMTPException as err:
            if self.logger: self.logger.debug('Check availability with error {0}:{1}'.format(type(err), err))
        except IOError as err:
            if self.logger: self.logger.debug('Network connection with SMTP server has error {0}:{1}'.format(type(err), err))
        else:
            if resHelo[0]>399:
                self.logger.debug('SMTP server returns code :"{0}" message:"{1}"'.format(*resHelo))
            else: return True

    def prepareMessage(self, filesList, recipients,act):
        try:
            action = {'ATTACH':self.__attachedMsg,
                      'NOTICE':self.__noticeMsg}[act.upper()]
            action(filesList)
            self.msg['Subject'] = 'mSender[{0}].Incoming file(s)'.format(act)
            self.msg['Content-Type'] = 'text/plan; charset=utf-8'
            self.msg['Content-Transfer-Encoding'] = 'quoted-printable'
            self.msg['From'] = self.fromAddr
            self.msg['To'] = ', '.join(recipients)
        except Exception as err:
            if self.logger: self.logger.debug('Message prepared with error {0}:{1}'.format(type(err), err))
        else:
            return True

    def sendMessage(self):
        try:
            self.SMTP.sendmail(self.msg['From'], self.msg['To'], self.msg.as_string())
        except smtplib.SMTPRecipientsRefused as err:
            if self.logger: self.logger.debug('Recipients was refused. Check email address {0}:{1}'.format(type(err), err))
        except smtplib.SMTPException as err:
            if self.logger: self.logger.debug('Message sent with error {0}:{1}'.format(type(err), err))
        else:
            return True


    def serverQuit(self):
        self.SMTP.quit()

    def __attachedMsg(self,filesList):
        self.msg = MIMEMultipart()
        for file_ in filesList:
            att = MIMEBase('application','octet-stream')
            with open(file_,'rb') as f:
                context_ = f.read()
            att.set_payload(context_)
            encoders.encode_base64(att)
            att.add_header('Content-Disposition','attachment', filename=file_)
            self.msg.attach(att)

    def __noticeMsg(self,filesList):
        self.msg = MIMEText('Incomming files: {0}'.format(', '.join(filesList)))


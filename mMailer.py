__author__ = 'Omic'

import smtplib

from email import encoders
from email.message import Message
from email.mime.text import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase

class mMailer():
    smtpServer = None
    smtpPort = None
    smtpUser = None
    smtpPasswd = None
    SMTP = None
    msg = None
    logger = None

    def __init__(self,smtpServer,smtpPort=25,smtpUser=None,smtpPasswd=None,fromaddr=None,logger=None):
        self.smtpServer=smtpServer
        self.smtpPort=smtpPort
        self.smtpUser=smtpUser
        self.smtpPasswd=smtpPasswd
        self.fromAddr=fromaddr
        self.logger=logger

    def CheckAilabilityServer(self):
        try:
            self.SMTP = smtplib.SMTP(self.smtpServer,self.smtpPort)
            return True
        except Exception as err:
            if self.logger is not None: self.logger.debug('{0}:{1}'.format(type(err),err))
            return False

    def PrepareMessage(self,filesList,recipients,act):
        try:
            action = {'ATTACH':self.__AttachedMsg,
                      'NOTICE':self.__NoticeMsg}[act.upper()]
            action(filesList)
            self.msg['Subject'] = 'mSender[{0}].Incoming file(s)'.format(act)
            self.msg['Content-Type'] = 'text/plan; charset=utf-8'
            self.msg['Content-Transfer-Encoding'] = 'quoted-printable'
            self.msg['From'] = self.fromAddr
            self.msg['To'] = ', '.join(recipients)
            return True
        except Exception as err:
            if self.logger is not None: self.logger.debug('{0}:{1}'.format(type(err),err))
            return False

    def SendMessage(self):
        try:
            self.SMTP.sendmail(self.msg['From'],self.msg['To'],self.msg.as_string())
            return True
        except Exception as err:
            if self.logger is not None: self.logger.debug('{0}:{1}'.format(type(err),err))
            return False

    def ServerQuit(self):
        self.SMTP.quit()

    def __AttachedMsg(self,filesList):
        self.msg = MIMEMultipart()
        for file_ in filesList:
            att = MIMEBase('application','octet-stream')#open(file_,'rb')
            with open(file_,'rb') as f:
                context_ = f.read()
            att.set_payload(context_)
            encoders.encode_base64(att)
            att.add_header('Content-Disposition','attachment',filename=file_)
            self.msg.attach(att)

    def __NoticeMsg(self,filesList):
        self.msg = MIMEText('Incomming files: {0}'.format(', '.join(filesList)))


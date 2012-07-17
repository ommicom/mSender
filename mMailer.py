__author__ = 'Omic'

import smtplib

from email.message import Message
from email.mime.text import MIMEText
from email.MIMEMultipart import MIMEMultipart

class mMailer():
    smtpServer = None
    smtpPort = None
    smtpUser = None
    smtpPasswd = None
    SMTP = None
    def __init__(self,smtpServer,smtpPort=25,smtpUser=None,smtpPasswd=None,fromaddr=None):
        self.smtpServer=smtpServer
        self.smtpPort=smtpPort
        self.smtpUser=smtpUser
        self.smtpPasswd=smtpPasswd
    def CheckAilabilityServer(self):
        try:
            self.SMTP = smtplib.SMTP(self.smtpServer,self.smtpPort)
            #if self.smtpUser is not None:
            #    self.SMTP.login(self.smtpUser,self.smtpPasswd)
            return True
        except :
            return False
    def PrepareMessage(self,filesList,recipients,act):
        try:
            action = {'ATTACH':self.__AttachedMsg,
                      'NOTICE':self.__NoticeMsg}[act.upper()]
            action(filesList,recipients)

            return True
        except :
            return False

    def SendMessage(self):
        return True

    def __AttachedMsg(self,filesList,recipients):
        #print 'attach',filesList,recipients
        pass

    def __NoticeMsg(self,filesList,recipients):
        #print 'notice',filesList,recipients
        pass


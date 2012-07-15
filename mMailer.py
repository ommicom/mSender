__author__ = 'Omic'

import smtplib
import email

class mMailer():
    __smtpServer = None
    __smtpPort = None
    __smtpUser = None
    __smtpPasswd = None
    def __init__(self,smtpServer,smtpPort=25,smtpUser=None,smtpPasswd=None):
        self.__smtpServer=smtpServer
        self.__smtpPort=smtpPort
        self.__smtpUser=smtpUser
        self.__smtpPasswd=smtpPasswd
    def CheckAilabilityServer(self):
        return True
    def PrepareMessage(self,filesList,recipients,act):
        pass
    def SendMessage(self):
        return True
    def __AttachedFileToMsg(self):
        pass

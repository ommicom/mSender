__author__ = 'Omic'

class mMailer():
    __smtpServer = None
    __smtpPort = None
    __smtpUser = None
    __smtpPasswd = None
    def __init__(self,smtpServer,smtpPort=21,smtpUser=None,smtpPasswd=None):
        self.__smtpServer=smtpServer
        self.__smtpPort=smtpPort
        self.__smtpUser=smtpUser
        self.__smtpPasswd=smtpPasswd
    def CheckAilabilityServer(self):
        pass
    def PrepareMessage(self,filesList,recipients,act):
        pass
    def SendMessage(self):
        pass
    def __AttachedFileToMsg(self):
        pass

__author__ = 'Omic'

class mConfigurator():
    __conf_name = None
    __conf_dict = dict()
    def __init__(self,confName='config'):
        self.__confName = confName
    def LoadConfig(self):
    #load and parse config file method
        pass
    def CreateConfig(self):
    #prepare and save config file method
        pass
    def GetConfig(self,secConf,paramConf=None):
    #get config variable method
        pass
    def __CheckConfig(self):
    #check configuration method
        pass

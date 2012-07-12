__author__ = 'Omic'

class mConfigurator():
<<<<<<< HEAD
    __conf_name = None
    __conf_dict = dict()
    def __init__(self,conf_name):
        self.__conf_name = conf_name
=======
    __confName = None
    __confDict = dict()
    def __init__(self,confName='config'):
        self.__confName = confName
>>>>>>> 6c63ed676c9e76ca8674747f69d822ad3ad773b9
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

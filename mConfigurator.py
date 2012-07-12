__author__ = 'Omic'

import json

class mConfigurator():
    __conf_name = None
    __conf_dict = dict()
    def __init__(self,confName='config'):
        self.__confName = confName
    def LoadConfig(self):
    #load and parse config file
        pass
    def CreateConfig(self):
    #prepare and save config file
        pass
    def GetConfigParam(self,secConf,paramConf):
    #get config variable
        pass
    def GetConfig(self,secConf):
        res = list()
        return res
    def __CheckConfig(self):
    #check configuration method
        pass

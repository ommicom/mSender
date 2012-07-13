__author__ = 'Omic'

import json

class mConfigurator():
    __jconf = None

    def __init__(self,conf):
        self.__conf = conf

    def LoadConfig(self):
        res = None
        try:
            self.__jconf = json.loads(self.__conf)
            self.__CheckConfig(self.__jconf)
            res = True
        except ValueError as err:
            res = False
            #print '{0}:{1}'.format(type(err),err)
        finally:
            return res

    def GetServerParam(self):
        return self.__jconf['server']['smtp'],self.__jconf['server']['port'],self.__jconf['server']['user'],self.__jconf['server']['passwd']

    def GetLists(self):
        return self.__jconf['lists']

    def GetMasks(self,list):
        return self.__jconf['lists'][list]['mask']

    def GetRecipients(self,list):
        return self.__jconf['lists'][list]['recipients']

    def GetAction(self,list):
        return self.__jconf['lists'][list]['action']

    def __CheckConfig(self):
    #check configuration method
        pass

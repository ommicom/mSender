__author__ = 'Omic'
__VERSION__ = '0.0.1'

import sys
import os
import argparse

import mConfigurator
import mMaskFiler
import mMailer
import mSenderExcept

def main(argv=None):
    parser = argparse.ArgumentParser(prog='mSender')
    parser.add_argument('-v','--version',action='version',help='print version mSender',version='mSender version {0}'.format(__VERSION__))
    parser.add_argument('-c','--config',action='store',help='name configuration for load',default='config')
    args = parser.parse_args()

    try:
        if os.path.exists(args.config)==False: raise mSenderExcept.ESenderConfigExcept('Configuration "{0}" not exist'.format(args.config))
        Config = mConfigurator.mConfigurator(args.config)
        if Config.LoadConfig()==False: raise mSenderExcept.ESenderConfigExcept('Configuration "{0}" not load'.format(args.config))
        Mailer = mMailer.mMailer(Config.GetConfigParam('server','smtp'),Config.GetConfigParam('server','port'),Config.GetConfigParam('server','user'),Config.GetConfigParam('server','passwd'))
        if Mailer.CheckAilabilityServer()==False: raise mSenderExcept.ESenderMailerExcept('SMTP server not available')
        Filer = mMaskFiler.mMaskFiler()
        masksList = Config.GetConfig('masks') #get all masks
        for mask in masksList:
            filesList = Filer.GetFilesList(mask) #get name of files
            if len(filesList)<1: continue
            else:
                recipients = Config.GetConfigParam(mask,'recipients')
                action = Config.GetConfigParam(mask,'action')
                Mailer.PrepareMessage(filesList,recipients,act)
                if Mailer.SendMessage()==False: raise mSenderExcept.ESenderMailerExcept('Sending message not successful')

        print 'Done!'
    except mSenderExcept.ESenderConfigExcept as err:
        print '{0}:{1}'.format(type(err),err)
    except mSenderExcept.ESenderMailerExcept as err:
        print '{0}:{1}'.format(type(err),err)

if __name__ =='__main__':
    sys.exit(main())

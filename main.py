__author__ = 'Omic'
__version__ = '0.0.1'

import os
import argparse

import mConfigurator
import mMaskFiler
import mMailer
import mSenderExcept

def main(argv=None):
    parser = argparse.ArgumentParser(prog='mSender')
    parser.add_argument('-v','--version',action='version',help='print version mSender',version='mSender version {0}'.format(__version__))
    parser.add_argument('-c','--config',action='store',help='name configuration for load',default='config')
    args = parser.parse_args()

    try:
        if os.path.exists(args.config)==False: raise mSenderExcept.ESenderConfigExcept('Configuration "{0}" not exist'.format(args.config))
        conf = open(args.config,'r').read()
        Config = mConfigurator.mConfigurator(conf)
        if Config.LoadConfig()==False: raise mSenderExcept.ESenderConfigExcept('Configuration "{0}" not load'.format(args.config))
        serverParam = Config.GetServerParam()
        Mailer = mMailer.mMailer(serverParam[0],serverParam[1],serverParam[2],serverParam[3])
        if Mailer.CheckAilabilityServer()==False: raise mSenderExcept.ESenderMailerExcept('SMTP server not available')
        Filer = mMaskFiler.mMaskFiler()
        lists = Config.GetLists()
        for list_ in lists:
            masks = Config.GetMasks(list_)
            filesList = Filer.GetFilesList(masks)
            if len(filesList)<1: continue
            else:
                recipients = Config.GetRecipients(list_)
                action = Config.GetAction(list_)
                Mailer.PrepareMessage(filesList,recipients,act)
                if Mailer.SendMessage()==False: raise mSenderExcept.ESenderMailerExcept('Sending message not successful')
                Filer.MarkFiles(filesList)

        print 'Done!'
    except mSenderExcept.ESenderConfigExcept as err:
        print '{0}:{1}'.format(type(err),err)
    except mSenderExcept.ESenderMailerExcept as err:
        print '{0}:{1}'.format(type(err),err)

if __name__ =='__main__':
    main()

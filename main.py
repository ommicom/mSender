__author__ = 'Omic'
__VERSION__ = '0.0.1'

import sys
import os
import argparse

import mConfigurator
import mLoger
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
        Mailer = mMailer.mMailer(Config.GetConfig('server','smtp'),Config.GetConfig('server','port'),Config.GetConfig('server','user'),Config.GetConfig('server','passwd'))
        if Mailer.CheckAilabilityServer()==False: raise mSenderExcept.ESenderMailerExcept('SMTP server not availability')

    except mSenderExcept.ESenderConfigExcept as err:
        print '{0}:{1}'.format(type(err),err)
    except mSenderExcept.ESenderMailerExcept as err:
        print '{0}:{1}'.format(type(err),err)

if __name__ =='__main__':
    sys.exit(main())

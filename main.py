__author__ = 'Omic'
__version__ = '0.0.1'

import os
import sys
import argparse
import json
import glob
import shutil

import mMailer
import mSenderExcept

BAK_DIRECTORY = 't:\BAK'

def checkConfig(conf):
    pass

def main(argv=None):
    listFiles = list()

    parser = argparse.ArgumentParser(prog='mSender')
    parser.add_argument('-v','--version',action='version',help='print version mSender',version='mSender version {0}'.format(__version__))
    parser.add_argument('-c','--config',action='store',help='name configuration for load',default='config')
    args = parser.parse_args()

    try:
        if os.path.exists(args.config)==False: raise mSenderExcept.ESenderConfigExcept('Configuration "{0}" not exist'.format(args.config))
        conf = json.loads(open(args.config,'r').read())
        if(checkConfig(conf)==False): raise mSenderExcept.ESenderConfigExcept('Configuration "{0}" have mistake(s)'.format(args.conf))
        Mailer = mMailer.mMailer(conf['server']['smtp'],conf['server']['port'],conf['server']['user'],conf['server']['passwd'])
        if Mailer.CheckAilabilityServer()==False: raise mSenderExcept.ESenderMailerExcept('SMTP server not available')
        lists = conf['lists']
        for list_ in lists:
            masks = lists[list_]['mask']
            for mask in masks:
                listFiles+=glob.glob(mask)
            if len(listFiles)<1: continue
            Mailer.PrepareMessage(listFiles,lists[list_]['recipients'],lists[list_]['action'])
            if Mailer.SendMessage()==False: raise mSenderExcept.ESenderMailerExcept('Sending message not successful')
            for file_ in listFiles:
                shutil.move(file_,conf['bakdir'])
            listFiles = []

        print 'Done!'
    except mSenderExcept.ESenderConfigExcept as err:
        print '{0}:{1}'.format(type(err),err)
    except mSenderExcept.ESenderMailerExcept as err:
        print '{0}:{1}'.format(type(err),err)
    #except KeyError as err:
    #    print '{0}:{1}'.format(type(err),err)

if __name__ =='__main__':
    sys.exit(main())

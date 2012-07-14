__author__ = 'Omic'
__version__ = '0.0.1'

import os
import sys
import argparse
import json
import glob
import shutil


import mMailer


def checkConfig(conf):
    return True

def main(argv=None):
    listFiles = list()

    parser = argparse.ArgumentParser(prog='mSender')
    parser.add_argument('-v','--version',action='version',help='print version mSender',version='mSender version {0}'.format(__version__))
    parser.add_argument('-c','--config',action='store',help='name configuration for load',default='config')
    args = parser.parse_args()

    try:
        if not os.path.exists(args.config):
            raise IOError('Configuration "{0}" not exist'.format(args.config))

        with open(args.config,'r') as conf_file:
            preconf = conf_file.read()
        conf = json.loads(preconf)

        if not checkConfig(conf):
            raise BaseException('Configuration "{0}" have mistake(s)'.format(args.config))
        Mailer = mMailer.mMailer(conf['server']['smtp'],conf['server']['port'],conf['server']['user'],conf['server']['passwd'])
        if not Mailer.CheckAilabilityServer():
            raise BaseException('SMTP server not available')
        lists = conf['lists']
        for list_ in lists:
            masks = lists[list_]['mask']
            for mask in masks:
                listFiles+=glob.glob(mask)
            if len(listFiles)<1: continue
            Mailer.PrepareMessage(listFiles,lists[list_]['recipients'],lists[list_]['action'])
            if not Mailer.SendMessage():
                raise BaseException('Sending message not successful')
            for file_ in listFiles:
                shutil.move(file_,conf['bakdir'])
            listFiles = []

        print 'Done!'
    except IOError as err:
        print '{0}:{1}'.format(type(err),err)
    except BaseException as err:
        print '{0}:{1}'.format(type(err),err)


if __name__ =='__main__':
    sys.exit(main())

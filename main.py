__author__ = 'Omic'
__version__ = '0.0.2'

import sys
import os
import argparse
import glob
import shutil
import logging

import mmailer

LOG_HANDLER = {'FILE':logging.FileHandler('msender.log'),
               'CON':logging.StreamHandler(sys.stdout)}
LOG_FORMATTER = logging.Formatter('%(asctime)s.%(msecs)d\t%(lineno)d\t%(message)s')
LOGMODE_DEFAULT = 'CON'

def main():
    listFiles = list()

    parser = argparse.ArgumentParser(prog='mSender')
    parser.add_argument('-v','--version',action='version',help='print version mSender',version='mSender version {0}'.format(__version__))
    args = parser.parse_args()
    logger = logging.getLogger('mSender')
    logger.setLevel(logging.DEBUG)

    try:
        from configs import config as config
    except ImportError as err:
        logger.addHandler(LOG_HANDLER[LOGMODE_DEFAULT])
        logger.debug('{0}:{1}'.format(type(err),'Can\'t load configuration'))
        sys.exit(0)

    server_ = config['server']
    lists = config['lists']

    logger.addHandler(LOG_HANDLER.get(config['logmode'],LOGMODE_DEFAULT))
    logger.handlers[0].setFormatter(LOG_FORMATTER)

    try:
        if not os.path.isdir(config['watchdir']):
            raise EnvironmentError('Watch directory "{0}" not exist'.format(config['watchdir']))
        if not os.path.isdir(config['bakdir']):
            raise EnvironmentError('Bak directory "{0}" not exist'.format(config['bakdir']))
        os.chdir(config['watchdir'])
    except EnvironmentError as err:
        logger.debug('{0}:{1}'.format(type(err),err))
        sys.exit(0)

    mailer = mmailer.mMailer(server_['smtp'],server_['port'],server_['user'],server_['passwd'],server_['fromaddr'],logger)
    try:
        if not mailer.checkAilabilityServer():
            raise Exception('SMTP server not available')
        for list_ in lists:
            masks = lists[list_]['mask']
            for mask in masks:
                listFiles+=glob.glob(mask)
            if len(listFiles)<1:continue
            if not mailer.prepareMessage(listFiles,lists[list_]['recipients'],lists[list_]['action']):
                raise Exception('Message for sending not prepare')
            if not mailer.sendMessage():
                raise Exception('Sending message not successful')
            for file_ in listFiles:
                shutil.move(file_,config['bakdir'])
            logger.debug('{0}: Sent file(s):{1}\tto:{2}\taction:{3}'.format(list_,listFiles,lists[list_]['recipients'],lists[list_]['action']))
            listFiles = []
        mailer.serverQuit()
    except Exception as err:
        logger.debug('{0}:{1}'.format(type(err),err))
        sys.exit()

if __name__ =='__main__':
    sys.exit(main())

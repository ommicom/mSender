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
WATCH_DEFAULT = os.getcwd()+'\\watch'
BAK_DEFAULT = os.getcwd()+'\\bak'
LOGMODE_DEFAULT = 'CON'
FROMADDR_DEFAULT = 'omsk@sdm.ru'
ACTION_DEFAULT = 'NOTICE'
SMTP_SERVER_DEFAULT = '127.0.0.1'
SMTP_PORT_DEFAULT = 25

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

    watch_dir = config.get('watchdir',WATCH_DEFAULT)
    bak_dir = config.get('bakdir',BAK_DEFAULT)
    if not os.path.isdir(watch_dir): os.mkdir(watch_dir)
    if not os.path.isdir(bak_dir): os.mkdir(bak_dir)

    smtp_server = server_.get('smtp',SMTP_SERVER_DEFAULT)
    smtp_port = server_.get('port',SMTP_PORT_DEFAULT)
    smtp_user = server_.get('user',None)
    smtp_passwd = server_.get('passwd',None)
    smtp_addr = server_.get('fromaddr',FROMADDR_DEFAULT)

    mailer = mmailer.mMailer(smtp_server,smtp_port,smtp_user,smtp_passwd,smtp_addr)

    if not mailer.checkAvailabilityServer():
        logger.error('SMTP server {0}:{1} not availability'.format(smtp_server,smtp_port))
        sys.exit()
    for list_ in lists:
        listFiles = []
        listRecipietns = []
        masks = lists[list_]['mask']
        for mask in masks:
            listFiles+=glob.glob(mask)
        if len(listFiles)<1:continue
        listRecipients = lists[list_]['recipients']
        action = litsts[list_].get('action',ACTION_DEFAULT)
        if not mailer.prepareMessage(listFiles,listRecipietns,action):
            logger.error('Message for sending not prepare')
            sys.exit()
        if not mailer.sendMessage():
            logger.error('Sending message not successful')
            sys.exit()
        for file_ in listFiles:
            shutil.move(file_,config['bakdir'])
        logger.debug('{0}: Sent file(s):{1}\tto:{2}\taction:{3}'.format(list_,listFiles,lists[list_]['recipients'],lists[list_]['action']))
    mailer.serverQuit()

if __name__ =='__main__':
    sys.exit(main())

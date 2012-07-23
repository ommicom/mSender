# -*- coding: utf-8 -*-
__author__ = 'Omic'
__version__ = '0.0.4'

import sys
import os
import argparse
import glob
import shutil
import logging

import mmailer

LOG_HANDLER = {'FILE':logging.FileHandler('msender.log'),'CON':logging.StreamHandler(sys.stdout)}
LOG_FORMATTER = logging.Formatter('%(asctime)s\t%(levelname)s\t%(lineno)d\t%(message)s')
LOG_LEVEL = {'DEBUG':logging.DEBUG,'INFO':logging.INFO,'WARNING':logging.WARNING,'ERROR':logging.ERROR,'CRITICAL':logging.CRITICAL,
             'NOTSET':logging.NOTSET}

WATCH_DEFAULT = os.getcwd()+'\\watch'
BAK_DEFAULT = os.getcwd()+'\\bak'

MASK_DEFAULT = ['*.*']

LOGOUTLET_DEFAULT = LOG_HANDLER['FILE']
LOGLEVEL_DEFAULT = LOG_LEVEL['DEBUG']

FROMADDR_DEFAULT = 'omsk@sdm.ru'
SMTP_SERVER_DEFAULT = '127.0.0.1'
SMTP_PORT_DEFAULT = 25
SMTP_AUTH = False
SMTP_TLS = False
ACTION_DEFAULT = 'NOTICE'

def main():
    listFiles = list()

    parser = argparse.ArgumentParser(prog='mSender')
    parser.add_argument('-v', '--version', action='version', help='print version mSender', version='mSender version {0}'.format(__version__))
    args = parser.parse_args()
    logger = logging.getLogger()

    try:
        from configs import config as config
    except ImportError as err:
        logger.addHandler(LOGOUTLET_DEFAULT)
        logger.error('{0}:{1}'.format(type(err), 'Can\'t load configuration'))
        sys.exit(0)

    server_ = config['server']
    lists = config['lists']
    log = config['log']

    logger.setLevel(LOG_LEVEL.get(log['loglevel'].upper(), LOGLEVEL_DEFAULT))
    logger.addHandler(LOG_HANDLER.get(log['logoutlet'].upper(), LOGOUTLET_DEFAULT))
    logger.handlers[0].setFormatter(LOG_FORMATTER)

    watchDir = config.get('watchdir', WATCH_DEFAULT)
    bakDir = config.get('bakdir', BAK_DEFAULT)
    if not os.path.isdir(watchDir):
        os.mkdir(watchDir)
    if not os.path.isdir(bakDir):
        os.mkdir(bakDir)
    os.chdir(watchDir)

    smtpServer = server_.get('smtp', SMTP_SERVER_DEFAULT)
    smtpPort = server_.get('port', SMTP_PORT_DEFAULT)
    smtpUser = server_.get('user', None)
    smtpPasswd = server_.get('passwd', None)
    smtpAddr = server_.get('fromaddr', FROMADDR_DEFAULT)
    smtpAuth = server_.get('auth', SMTP_AUTH)
    smtpTLS = server_.get('tls', SMTP_TLS)

    mailer = mmailer.mMailer(smtpServer, smtpPort, smtpUser, smtpPasswd, smtpAddr, smtpAuth, smtpTLS, logger)

    if not mailer.checkAvailabilityServer():
        logger.error('SMTP server {0}:{1} not ready for sending message'.format(smtpServer, smtpPort))
        sys.exit()

    for list_ in lists:
        listFiles = []
        listRecipients = []
        masks = lists[list_].get('mask', MASK_DEFAULT)
        for mask in masks:
            listFiles += glob.glob(mask)
        if not listFiles:
            continue
        if 'recipients' not in lists[list_]:
            logger.error('List of recipients in list "{0}" wasn\'t defined'.format(list_))
            continue
        listRecipients = lists[list_]['recipients']
        action = lists[list_].get('action', ACTION_DEFAULT)
        if not mailer.prepareMessage(listFiles, listRecipients, action):
            logger.error('Message to the list "{0}" wasn\'t sent'.format(list_))
            continue
        if not mailer.sendMessage():
            logger.error('Sending a message to the list "{0}" of unsuccessful'.format(list_))
            continue
        for file_ in listFiles:
            shutil.move(file_, bakDir)
        logger.info('{0}: Sent file(s):{1}\tto:{2}\taction:{3}'.format(list_, listFiles, lists[list_]['recipients'], lists[list_]['action']))
    mailer.serverQuit()

if __name__ =='__main__':
    sys.exit(main())

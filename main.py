__author__ = 'Omic'
__version__ = '0.0.2'

import sys
import argparse
import glob
import shutil
import logging

import mMailer

LOG_HANDLER = {'FILE':logging.FileHandler('msender.log'),
               'CON':logging.StreamHandler(sys.stdout)}
LOG_FORMATTER = logging.Formatter('%(asctime)s.%(msecs)d\t%(lineno)d\t%(message)s')

def main():
    listFiles = list()

    parser = argparse.ArgumentParser(prog='mSender')
    parser.add_argument('-v','--version',action='version',help='print version mSender',version='mSender version {0}'.format(__version__))
    args = parser.parse_args()
    logger = logging.getLogger('mSender')
    logger.setLevel(logging.DEBUG)

    try:
        import configs

        server_ = configs.server_
        lists = configs.lists

        logger.addHandler(LOG_HANDLER.get(configs.logmode,logging.StreamHandler(sys.stdout)))
        logger.handlers[0].setFormatter(LOG_FORMATTER)

        Mailer = mMailer.mMailer(server_['smtp'],server_['port'],server_['user'],server_['passwd'],server_['fromaddr'])
        if not Mailer.CheckAilabilityServer():
            raise BaseException('SMTP server not available')

        for list_ in lists:
            masks = lists[list_]['mask']
            for mask in masks:
                listFiles+=glob.glob(mask)
            if len(listFiles)<1:continue
            logger.debug('SMTP server {0}:{1} user:{2}'.format(server_['smtp'],server_['port'],server_['user']))
            if not Mailer.PrepareMessage(listFiles,lists[list_]['recipients'],lists[list_]['action']):
                raise BaseException('Message for sending not prepare')
            if not Mailer.SendMessage():
                raise BaseException('Sending message not successful')
            for file_ in listFiles:
                shutil.move(file_,configs.bakdir)
            logger.debug('Sent file(s):{0}\tto:{1}\taction:{2}'.format(listFiles,lists[list_]['recipients'],lists[list_]['action']))
            listFiles = []

    except ImportError as err:
        logger.debug('{0}:{1}'.format(type(err),err))
    except KeyError as err:
        logger.debug('{0}:{1}'.format(type(err),err))
    except BaseException as err:
        logger.debug('{0}:{1}'.format(type(err),err))

if __name__ =='__main__':
    sys.exit(main())

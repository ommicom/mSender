from cookielib import logger

__author__ = 'Omic'
__version__ = '0.0.2'

import sys
import argparse
import glob
import shutil
import logging
import functools


import mMailer

LOG_HANDLER = {'FILE':logging.FileHandler('msender.log'),
               'CON':logging.StreamHandler(sys.stdout)}
logger = logging.getLogger('mSender')
logger.setLevel(logging.DEBUG)

def putToLog(function):
    @functools.wraps(function)
    def wrapper(*args,**kwargs):
        log = function.__name__

        res = exception = None
        try:
            res = func(*args,**kwargs)
            return res
        except Exception as err:
            exception = err
        finally:
            log +='!'
        logger.debug(log)


def main(argv=None):
    listFiles = list()

    parser = argparse.ArgumentParser(prog='mSender')
    parser.add_argument('-v','--version',action='version',help='print version mSender',version='mSender version {0}'.format(__version__))
    args = parser.parse_args()

    try:
        import configs

        server_ = configs.server_
        lists = configs.lists
        log = configs.log

        logger.addHandler(LOG_HANDLER.get(log['logmod'],logging.StreamHandler(sys.stdout)))

        Mailer = mMailer.mMailer(server_['smtp'],server_['port'],server_['user'],server_['passwd'])
        if not Mailer.CheckAilabilityServer():
            raise BaseException('SMTP server not available')

        for list_ in lists:
            masks = lists[list_]['mask']
            for mask in masks:
                listFiles+=glob.glob(mask)
            if len(listFiles)<1:continue
            Mailer.PrepareMessage(listFiles,lists[list_]['recipients'],lists[list_]['action'])
            if not Mailer.SendMessage():
                raise BaseException('Sending message not successful')
            for file_ in listFiles:
                shutil.move(file_,configs.bakdir)
            listFiles = []

        print 'Done!'
    except ImportError as err:
        print '{0}:{1}'.format(type(err),err)
    except KeyError as err:
        print '{0}:{1}'.format(type(err),'Config have errors')
    except BaseException as err:
        print '{0}:{1}'.format(type(err),err)

if __name__ =='__main__':
    sys.exit(main())

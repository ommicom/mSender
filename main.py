__author__ = 'Omic'
__version__ = '0.0.1'

import os
import argparse
import json

import mMailer
import mSenderExcept

def checkConfig(conf):
    pass

def main(argv=None):
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
        #list_ = [list_ in ]




        print 'Done!'

    except mSenderExcept.ESenderConfigExcept as err:
        print '{0}:{1}'.format(type(err),err)
    #except KeyError as err:
    #    print '{0}:{1}'.format(type(err),err)

if __name__ =='__main__':
    main()

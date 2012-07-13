__author__ = 'Omic'
__version__ = '0.0.1'

import os
import argparse

import mSenderExcept

def main(argv=None):
    parser = argparse.ArgumentParser(prog='mSender')
    parser.add_argument('-v','--version',action='version',help='print version mSender',version='mSender version {0}'.format(__version__))
    parser.add_argument('-c','--config',action='store',help='name configuration for load',default='config')
    args = parser.parse_args()

    try:
        if os.path.exists(args.config)==False: raise mSenderExcept.ESenderConfigExcept('Configuration "{0}" not exist'.format(args.config))
        conf = open(args.config,'r').read()


        print 'Done!'

    except mSenderExcept.ESenderConfigExcept as err:
        print '{0}:{1}'.format(type(err),err)

if __name__ =='__main__':
    main()

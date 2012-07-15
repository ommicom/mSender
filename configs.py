__author__ = 'omic'

server_={'smtp':'127.0.0.1','port':25,'user':'','passwd':''}
lists={'list1':{'mask':['*a.*','*b.*'],'recipients':['mail1@mail.mail','mail2@mail.mail'],'action':'NOTICE'},
       'list2':{'mask':['*c.*','*d.*'],'recipients':['mail1@mail.mail','mail3@mail.mail'],'action':'ATTACH'}}
bakdir = 't:\bak'
logmod = 0 # 0 - off logging|1 - logging to file|2 - logging to console

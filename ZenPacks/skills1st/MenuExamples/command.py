import Globals
import os
from Products.ZenUtils.Utils import executeCommand
from Products.ZenUtils.jsonutils import unjson
from Products.Zuul import getFacade
from Products.ZenUI3.browser.streaming import StreamingView
import logging
log = logging.getLogger('zen.ZenPack')

class MyPredefinedCommandView(StreamingView):

    def stream(self):
# Setup a logging file
        logfile = open('/usr/local/zenoss/zenoss/log/example_logging.log', 'a')
        logfile.write('Start logging')
        data = unjson(self.request.get('data'))
        logfile.write(' data is \n' % (data))
        try:
            args = data['args']
            logfile.write('Argument is %s \n' % (args))
            arg3 = args
        except:
            logfile.write(' No args \n')
            arg3 = ''
        try:
            uids = data['uids']
            logfile.write('uids is %s \n' % (uids))
            arg4 = uids
        except:
            logfile.write('No uids \n')
            arg4 = ''
#        facade = getFacade('device', self.context)
#        organizer = facade._getObject(uids[0])
#        logfile.write(' organizer is %s ' % (organizer))

        libexec = os.path.join(os.path.dirname(__file__), 'libexec')

        arg1 = "Hello"
        arg2 = "World"

# Put the  script in the libexec directory of the ZenPack
        myPredefinedCmd1 = [
             libexec + '/mywrapper_script1',
            arg1, arg2, arg3, arg4
        ]
        logfile.write(' myPredefinedCmd1 is %s ' % (myPredefinedCmd1))
        self.write('Preparing my command...')
        result = executeCommand(myPredefinedCmd1, None, write=self.write)
        self.write('End of command...')
        logfile.close()
        return result



import Globals
import os
from Products.ZenUtils.Utils import executeCommand
from Products.ZenUtils.jsonutils import unjson
from Products.Zuul import getFacade
from Products.ZenUI3.browser.streaming import StreamingView

class MyPredefinedCommandView(StreamingView):

    def stream(self):
        data = unjson(self.request.get('data'))
        uids = data['uids']
        facade = getFacade('device', self.context)
        organizer = facade._getObject(uids[0])

        libexec = os.path.join(os.path.dirname(__file__), 'libexec')

        arg1 = "Hello"
        arg2 = "World"

# Put the  script in the libexec directory of the ZenPack
        myPredefinedCmd1 = [
             libexec + '/mywrapper_script1',
            arg1, arg2
        ]
        result = executeCommand(myPredefinedCmd1, None, None)
        return result



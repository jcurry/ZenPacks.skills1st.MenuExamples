from Products.ZenUtils.Ext import DirectRouter, DirectResponse
from Products import Zuul

# The class name here must match up with the class name in a
#  browser:directRouter stanza in configure.zcml (ie. ExampleDeviceRouter )
# It must also match with the name specified in a js file which uses
#   this router class  - see add_example_device_option.js
#        Zenoss.remote.ExampleDeviceRouter.add_ExampleDevice(opts

class ExampleDeviceRouter(DirectRouter):
    def _getFacade(self):

        # The parameter in the next line - exampleDevice - must match with 
        #   the name field in an adapter stanza in configure.zcml

        return Zuul.getFacade('exampleDevice', self.context)

    # The method name - add_ExampleDevice - and its parameters - must match with 
    #   the last part of the call for Zenoss.remote.ExampleDeviceRouter.add_ExampleDevice
    #   in the javascript file add_example_device_option.js . The parameters will be
    #   populated by the items defined in the js file.

    def add_ExampleDevice(self, deviceIp, community, comment):
        facade = self._getFacade()

        # The facade name in the next line & its parameters must match with a method defined
        #   in facades.py (ie. add_ExampleDevice(deviceIp, community, comment) )

        success, message = facade.add_ExampleDevice(deviceIp, community, comment)

        if success:
            return DirectResponse.succeed(jobId=message)
        else:
            return DirectResponse.fail(message)

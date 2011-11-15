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

class myAppRouter(DirectRouter):
    def _getFacade(self):

        # The parameter in the next line - myAppAdapter - must match with 
        #   the name field in an adapter stanza in configure.zcml

        return Zuul.getFacade('myAppAdapter', self.context)

    # The method name - myRouterFunc - and its parameters - must match with 
    #   the last part of the call for Zenoss.remote.myAppRouter.myRouterFunc
    #   in the javascript file myFooterMenu.js . The parameters will be
    #   populated by the items defined in the js file.

    # Note that the router function has 2 parameters, comments and rackSlot
    #  that are passed as the "opts" parameters from myFooterMenu.js.  The 
    #  values of these fields were provided by the form input.

    def myRouterFunc(self, comments, rackSlot):
        facade = self._getFacade()

        # The object that is being operated on is in self.context

        ob = self.context

        # The facade name in the next line & its parameters must match with a method defined
        #   in facades.py (ie. myFacadeFunc(ob, comments, rackSlot) )
        # Note that facade.myFacadeFunc needs 3 parameters as we need to pass the
        #    object as well as the comments and rackSlot attribute values.

        success, message = facade.myFacadeFunc(ob, comments, rackSlot)

        if success:
            return DirectResponse.succeed(message)
        else:
            return DirectResponse.fail(message)

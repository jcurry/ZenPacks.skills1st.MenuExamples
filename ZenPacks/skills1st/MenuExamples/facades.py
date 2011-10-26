import os
import logging
log = logging.getLogger('zen.ExampleDeviceFacade')

from zope.interface import implements

from Products.Zuul.facades import ZuulFacade
from Products.Zuul.utils import ZuulMessageFactory as _t

from .interfaces import IExampleDeviceFacade

# The ZuulFacade class name, ExampleDeviceFacade, must match the name specified
#  in the factory field of an adapter stanza in configure.zcml
#  ie. ExampleDeviceFacade 
#
# The implements line must match that specified in the same adapter's "provides" field
#    and in interfaces.py, must match the IFacade class defined there ( ie. IExampleDeviceFacade )

class ExampleDeviceFacade(ZuulFacade):
    implements(IExampleDeviceFacade)

# The method name add_ExampleDevice and its parameters must match those defined in
#    interfaces.py and routers.py 
# It is the following method that ACTUALLY does the work of adding a device

    def add_ExampleDevice(self, deviceIp, community, comment):
        """Add a device of class ExampleDevice """

        deviceRoot = self._dmd.getDmdRoot("Devices")
        device = deviceRoot.findDeviceByIdExact(deviceIp)
        if device:
            return False, _t("A device named %s already exists." % deviceIp)

        zProperties = {
            'zSnmpCommunity': community,
            'zPythonClass': 'ZenPacks.skills1st.MenuExamples.ExampleDevice',
            }

        perfConf = self._dmd.Monitors.getPerformanceMonitor('localhost')
        
        # addDeviceCreationJob is a method defined in $ZENHOME/Products/ZenModel/PerformanceConf.py
        # Parameters here are not exhustive. discoverProto='snmp' ensures device is modeled as well
        #   as discovered into the Zope database

        jobStatus = perfConf.addDeviceCreationJob(
            deviceName=deviceIp,
            devicePath='/Example/TestClass',
            discoverProto='snmp',
            comments=comment,
            zProperties=zProperties)

        return True, jobStatus.id


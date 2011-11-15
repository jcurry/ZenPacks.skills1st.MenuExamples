###########################################################################################
#
# Author:               Jane Curry,  jane.curry@skills-1st.co.uk
# Date:                 September 26th, 2011
# Revised:              
#
# ZenPack to demonstrate ways of creating menus
###########################################################################################

# Nothing is required in this __init__.py, but it is an excellent place to do
# many things in a ZenPack.
#
# The example below which is commented out by default creates a custom subclass
# of the ZenPack class. This allows you to define custom installation and
# removal routines for your ZenPack. If you don't need this kind of flexibility
# you should leave the section commented out and let the standard ZenPack
# class be used.
#
# Code included in the global scope of this file will be executed at startup
# in any Zope client. This includes Zope itself (the web interface) and zenhub.
# This makes this the perfect place to alter lower-level stock behavior
# through monkey-patching.

import Globals

from Products.ZenModel.ZenPack import ZenPack as ZenPackBase
from Products.ZenUtils.Utils import unused

unused(Globals)


class ZenPack(ZenPackBase):
#
#     # All zProperties defined here will automatically be created when the
#     # ZenPack is installed.
#     packZProperties = [
#         ('zExampleString', 'default value', 'string'),
#         ('zExampleInt', 411, 'int'),
#         ('zExamplePassword', 'notsecure', 'password'),
#         ]

#
# Code that is run when the ZenPack is installed
#
     def install(self, dmd):
         ZenPackBase.install(self, dmd)
         #
         # To create an organizer when the ZenPack is installed, uncomment the next few lines
         #
         dc = dmd.Devices.createOrganizer('/Example/TestClass')
         dc.setZenProperty('zCollectorPlugins',
                                 ('zenoss.snmp.NewDeviceMap',
                                  'zenoss.snmp.DeviceMap',
                                  'zenoss.snmp.InterfaceMap',
                                  'zenoss.snmp.RouteMap',
                                  'community.snmp.ExampleSNMP',
                                  'community.snmp.ExampleHostResourcesSNMP',
                                  'community.cmd.ExampleCMD',))
         # If we want to use a Command modeler plugin, then cmd userid and password need to be setup
         dc.setZenProperty('zCommandUsername', 'mollie')
         dc.setZenProperty('zCommandPassword', 'fiddle')

         #
         # Ensure that properties for this organizer class will be of device object class ExampleDevice
         #
         dc.setZenProperty('zPythonClass', 'ZenPacks.skills1st.MenuExamples.ExampleDevice')
         #
         #Create an instance of this device class, checking first whether such a an instance exists

         if dc.devices._getOb('ExampleDevice1', None): return
         myInst = dc.createInstance('ExampleDevice1')
         myInst.setPerformanceMonitor('localhost')


# Code that is run when the ZenPack is removed

     def remove(self, dmd, leaveObjects=False):
         if not leaveObjects:
             # When a ZenPack is removed the remove method will be called with
             # leaveObjects set to False. This means that you likely want to
             # make sure that leaveObjects is set to false before executing
             # your custom removal code.
         #
         # Delete all instances of devices in /Example/TestClass - completely - including history and events
         #
             for dev in dmd.Devices.Example.TestClass.getSubDevices():
                 dev.deleteDevice(deleteStatus=True, deleteHistory=True, deletePerf=True)
         #
         # Now delete the device class organizer hierarchy we created
         #
         # Next line delete all subclasses too
         #
             dmd.Devices.manage_deleteOrganizer('/Devices/Example')

         ZenPackBase.remove(self, dmd, leaveObjects=leaveObjects)

#
# The rest is global stuff
#
import logging
log = logging.getLogger('zen.ZenPack')

import os.path


# Register the skins directory - we don't need this now if we put page template
#   files under browser/resources in Zenoss 3 style.  It IS needed if you want to 
#   find NEW pt files in the ZenPack's skins directory (all versions of Zenoss).
# Note from Zenoss 3.2 that pt files that OVERRIDE Core pt files may NOT be 
#   picked up from the skins directory (even with the skinsDir registered as below).  
#   pt files that override Core pt files should actively be "wired in" with
#     statements in a configure.zcml file
#
skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

# In older-style Zenoss 2.x  ZenPacks the pt files are under skins/<ZenPack name>
# The new Zenoss 3 convention is to put them under browser/templates and use the zcml files
#  to 'wire-in' this directory
#

#
# Create a new menu item in the left-hand menu for all devices
#
# The label of the menu is the 'name' parameter
# The 'action' parameter refers to a page template (.pt) file  (without the .pt) if using
#   Zenoss 2 skins directory or refers to the "name" field in a page stanza
#   if using Zenoss 3 browser/configure.zcml wiring.
#
# The 'permissions' field defines the permission that a role must have for this to be valid for a user
#
from AccessControl import Permissions
from Products.ZenModel.Device import Device

myExampleMenu1 = { 'id': 'myExampleMenu1',
        'name' : 'My Example Menu 1',
        'action' : 'myExampleMenuOne',
        'permissions' : ( Permissions.view,)
        }

# Add this menu for certain object classes.  Adding to "Device" means
# it is available for all subclasses of /Device

Device.factory_type_information[0]['actions'] += (myExampleMenu1,)




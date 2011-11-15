# Menu Examples ZenPack 
This README describes  the various ways to create different types of menus.

## ZenPack installation
On installation, an organizer is created for the device class /Example/TestClass.

Device properties are set for some standard modeler plugins and some plugins that
are provided by this ZenPack.  The zCommandUserName and zCommandPassword are set 
and the zPythonClass is set to ZenPacks.skills1st.MenuExamples.ExampleDevice.

A test device called ExampleDevice1 is created in this object class.

When the ZenPack is removed, all devices under /Example are removed as are
the /Example organizer and any suborganizers.

This is all achieved in __init__.py.

You may want to then change the IP address of ExampleDevice1 to some real device
that supports SNMP so you can model it.

## ExampleDevice and ExampleComponent
### Example Device

The object class, ExampleDevice, inherits from Device and has an extra relationship with 
a contained component called ExampleComponent.

The ExampleDevice object class has its factory information actions extended with
myExampleMenuTwo.

This object class also has a method to set the comment field for the device (which
is called by myDropDownMenu1).

### Example Component
The object class, ExampleComponent, uses the modeler plugin, ExampleHostResourcesSNMP, to get 
values for its extra attributes of devDescr, devStatus and devErrors.  These values are
obtained from a device using SNMP to query the host resources MIB.

The Example Components left-hand menu shows each valid hrDevice component that is
discovered.  ExampleComponent.py also adds "Example ComponentTemplate"  to the dropdown
Display menu for ExampleComponents (this simply collects an SNMP value for devErrors and
the ExampleComponent performance template is included as an object in the ZenPack).

## Extending the Display dropdown menus for a component
A number of menu options appear by default under the Display dropdown in the middle of
the page displaying details of a component.  Typically these options show Graphs, Events
and Details.

The old-style V2 way to add to this dropdown extends the factory_type_information actions
as described above, where the standard "objTemplates" action is added under the menu
heading of "Example Component Template".

The V3 way of adding menus to the Display dropdown uses a viewlet entry in 
browser/configure.zcml and a javascript file, amazing.js, under
browser/resources/js.  Note that the manager field in configure.zcml needs to be
manager="Products.ZenUI3.browser.interfaces.IHeadExtraManager" .

The menu simply produces an alert popup with the UID of the component.


## Left hand menus applicable to all devices
### menu1

This menu is defined in 2 different ways.  Look at the title of the page to see
whether it is being driven by action factory_type_information under the skins
subdirectory (old Zenoss 2.x style menus in myExampleMenuOne.pt) or whether it is being 
driven by Zenoss 3 browser/configure.zcml wiring.  

Both definitions display a table of device info (the V3 style includes an extra 
comments field), performance graphs for the device, and a table at the bottom showing 
which Groups a device is a member of.

The old-style menu is defined in the __init__.py in the base directory of the
ZenPack.  It requires View permission and it is added to the
factory actions of all devices. The definition of the layout is under
the skins/ZenPacks.skills1st.MenuExamples subdirectory in the myExampleMenuOne.pt file.
 
The new Zenoss 3 type of menu is defined in browser/configure.zcml as myExampleMenuOne. This
V3-style definitio is ONLY applicable for devices of object class ExampleDevice and the page
layout is in browser/templates/myExampleMenuOne.pt . 

The result of all this is that all devices should have a "My Example Menu 1" left-hand menu
but ExampleDevice objects have a slightly different page from all other devices.

### Modifications

The "Modifications" menu is a standard menu that this ZenPack overrides in 2 different ways.
Both are largely copies of the standard viewHistory.pt file in 
$ZENHOME/Products/ZenModel/skins/zenmodel.  As with menu1, there is a different
override for devices of object class ExampleDevice, as opposed to all other devices.  Examine
the title of the page to see which code is actually used.

The skins subdirectory has a copy of viewHistory.pt which simply has its title changed.

The browser/templates subdirectory has a viewHistory.pt with a different title and a small
modification to the odd/even test (see comments in code).  browser/configure.zcml also needs
an entry to point to browser/templates/viewHistory.pt which, in this case, limits this
particular override to devices of object class ExampleDevice.

The result of all this is that all devices should have an overriden "Modifications" left-hand 
menu but ExampleDevice objects have a slightly different page from all other devices.

## Left hand menus limited to specific devices
Menu2

The "My Example Menu 2" is only defined for devices of object class ExampleDevice and is
only defined in the V3-style combination of browser/configure.zcml and 
browser/templates/myExampleMenuTwo.pt.  It display a table of standard SNMP attributes
and the standard performance Graphs.

This menu only appears for devices of object class ExampleDevice.

## Adding menus via objects.xml
Menus can be delivered as objects in objects/objects.xml. mydropDownMenu1 and mydropDownMenu2
are delivered this way.  They are called from both versions of the myExampleMenuOne.pt file (both
the skins version and the browser/templates version) by the line
    menu_id string:ExampleOneMenuObjects_list
It is the "action" stanza in the menu item definition that must match with the "name" field of
an entry in browser/configure.zcml.  Both these menus are defined in Zenoss-3 style with
configure.zcml and pt files in browser/templates.  

mydropDownMenu1 is restricted for use only by devices of object class ExampleDevice 
(because it uses the createComment method which is only defined for the ExampleDevice object class).  
The result is that for devices of other object classes, the submit window simply hangs and can 
be closed harmlessly.
 
myDropDownMenu1 prompts for a Comment for the device and uses the createComment method to update
the comments attribute for the device.

For ExampleDevice devices note that after clicking the OK button, control is returned to the 
defaultdetails view as this is the default view as defined in the factory information for a device.

myDropDownMenu2 is valid for all devices and produces a popup with a few SNMP attributes.

## Extending the Add Device menu
The standard Zenoss Core menus have options to add a new device from the "+" dropdown menu 
at the top of the list of devices. It is possible to add an extra option to that menu that 
is specific for a particular device object class. This is done with a viewlet stanza in
browser/configure.zcml that points to a javascript file, add\_example\_device\_option.js

The javascript file creates a new Zenoss Action that prompts for deviceIp, community and
comment fields and then submits a job to create the new device. These fields are passed to
a router construct, Zenoss.remote.ExampleDeviceRouter.add\_ExampleDevice(opts,  ...........
The new Zenoss Action is "pushed" onto the existing adddevice menu.

routers.py in the base directory of the ZenPack, contains the definitions for routers and
their functions.  Typically a router calls a facade (defined in facades.py) which is the code
that actually does work.  Router names, their functions and their parameters must all match 
up between the router.py / facades.py entries and the javascript that calls the router.

zcml "wiring" is required in the top-level configure.zcml for the router and must provide
an adapter for the facade.  

interfaces.py (in the top-level directory) must have an entry for the interface for the 
facade, matching any functions and their parameters.


##Extending the Action menu for the device list
Run my Predefined Command

## Adding a new menu to the footer bar
myFooterMenu.js

##Adding extra items to a device's Action menu
deviceGearMenu.js

##Acknowledgements


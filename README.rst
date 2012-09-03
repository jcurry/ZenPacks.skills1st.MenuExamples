=====================
Menu Examples ZenPack 
=====================

Description
===========

This README describes  the various ways to create different types of menus.
The code started from the ZenPackTemplate work done by Chet Luther - see
https://github.com/zenoss/ZenPackTemplate

Requirements & Dependencies
===========================

    * Zenoss Versions Supported: 3.x and 4.2
    * External Dependencies: 
    * ZenPack Dependencies:
    * Installation Notes: Restart zenoss entirely after installation
    * Configuration:

Components
==========

Device classes and devices
--------------------------

On installation, an organizer is created for the device class /Example/TestClass.

Device properties are set for some standard modeler plugins and some plugins that
are provided by this ZenPack.  The zCommandUserName and zCommandPassword are set 
and the zPythonClass is set to ZenPacks.skills1st.MenuExamples.ExampleDevice.

A test device called ExampleDevice1 is created in this object class.

When the ZenPack is removed, all devices under /Example are removed as are
the /Example organizer and any suborganizers.

This is all achieved in \_\_init\_\_.py.

You may want to then change the IP address of ExampleDevice1 to some real device
that supports SNMP so you can model it.

ExampleDevice and ExampleComponent
----------------------------------

The object class, ExampleDevice, inherits from Device and has an extra relationship with 
a contained component called ExampleComponent.

There is also a command modeler plugin that gets hard disk information and populates the
_existing_ hardware relationship, harddisks, which shows as an extra component in the
left-hand menu.

The ExampleDevice object class has its factory information actions extended with
myExampleMenuTwo.

This object class also has a method, createComment, to set the comment field for the 
device (which is called by myDropDownMenu1).

The object class, ExampleComponent, uses the modeler plugin, ExampleHostResourcesSNMP, to get 
values for its extra attributes of devDescr, devStatus and devErrors.  These values are
obtained from a device using SNMP to query the host resources MIB. 

The Example Components left-hand menu shows each valid hrDevice component that is
discovered by the ExampleHostResourcesSNMP modeler.  ExampleComponent.py also adds 
"Example ComponentTemplate"  to the dropdown Display menu for ExampleComponents 
(this simply collects an SNMP value for devErrors and the ExampleComponent performance template 
is included as an object in the ZenPack).

An adapter entry is required in the top-level configure.zcml to provides links to the
info and interfaces entries for both the ExampleComponent and for the Hard Disk component.
interfaces.py contains  entries for each that defines the attributes to be displayed in the
Details dropdown option for the component.  info.py has entries for each describing the
nature of ecah attribute.

The layout for the ExampleComponent menu is under browser/resources/js in ExampleDevice.js
and describes the attributes to be displayed and how they will appear.  The Hard Disk menu
is also described in this same file.  A viewlet entry is required in browser/configure.zcml
to link to the javascript file.

Extending the Display dropdown menus for a component
-----------------------------------------------------

A number of menu options appear by default under the Display dropdown in the middle of
the page displaying details of a component.  Typically these options show Graphs, Events
and Details.

The old-style V2 way to add to this dropdown extends the factory\_type\_information actions
as described above, where the standard "objTemplates" action is added under the menu
heading of "Example Component Template".

The V3 way of adding menus to the Display dropdown uses a viewlet entry in 
browser/configure.zcml and a javascript file, amazing.js, under
browser/resources/js.  Note that the manager field in configure.zcml needs to be
manager="Products.ZenUI3.browser.interfaces.IHeadExtraManager" .

The menu simply produces an alert popup with the UID of the component.


Left hand menus applicable to all devices
-----------------------------------------
menu1

This menu is defined in 2 different ways.  Look at the title of the page to see
whether it is being driven by action factory\_type\_information under the skins
subdirectory (old Zenoss 2.x style menus in myExampleMenuOne.pt) or whether it is being 
driven by Zenoss 3 browser/configure.zcml wiring.  

Both definitions display a table of device info (the V3 style includes an extra 
comments field), performance graphs for the device, and a table at the bottom showing 
which Groups a device is a member of.

The old-style menu is defined in the \_\_init\_\_.py in the base directory of the
ZenPack.  It requires View permission and it is added to the
factory actions of all devices. The definition of the layout is under
the skins/ZenPacks.skills1st.MenuExamples subdirectory in the myExampleMenuOne.pt file.
 
The new Zenoss 3 type of menu is defined in browser/configure.zcml as myExampleMenuOne. This
V3-style definition is ONLY applicable for devices of object class ExampleDevice and the page
layout is in browser/templates/myExampleMenuOne.pt . 

The result of this is that all devices should have a "My Example Menu 1" left-hand menu
but ExampleDevice objects have a slightly different page from all other devices.

Modifications

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

The result of this is that all devices should have an overriden "Modifications" left-hand 
menu but ExampleDevice objects have a slightly different page from all other devices.

Left hand menus limited to specific devices
--------------------------------------------

Menu2

The "My Example Menu 2" is only defined for devices of object class ExampleDevice and is
only defined in the V3-style combination of browser/configure.zcml and 
browser/templates/myExampleMenuTwo.pt.  It display a table of standard SNMP attributes
and the standard performance Graphs.

This menu only appears for devices of object class ExampleDevice.

Adding menus via objects.xml
----------------------------

Menus can be delivered as objects in objects/objects.xml. mydropDownMenu1 and mydropDownMenu2
are delivered this way.  They are called from both versions of the myExampleMenuOne.pt file (both
the skins version and the browser/templates version) by the line

    menu\_id string:ExampleOneMenuObjects\_list

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

Extending the Add Device menu
------------------------------

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


Extending the Action menu for the device list
---------------------------------------------

The Infrastructure device list panel has an Action menu at the bottom of the navigator
tree. Actions chosen apply to any selected devices.  This menu has been extended to run a
predefined command that produces a popup window with the command output.

A viewlet entry is required in browser/configure.zcml that points to the javascript file
run\_my\_predefined\_command.js.  A page entry is also required to show the output from
the command, where the class field defines an entry in command.py (in the top-level
directory) to actually run the command. The MyPredefinedCommandView class in command.py
also demonstrates logging to a specified logfile ( $ZENHOME/log/example\_logging.log) 
and uses both literal parameters and parameters passed from the calling window.  The actual 
command is in the libexec subdirectory as /mywrapper\_script1.  It simply echos 4 parameters.

Adding a new menu to the footer bar
------------------------------------

A whole new menu can be added to the footer bar at the bottom of the navigation tree menu.
A viewlet entry is required in browser/Configure.zcml that points to the javascript file
myFooterMenu.js.  The menu has the standard "Model device" action, an action to run the same 
predefined command discussed earlier, and an option "Set device comment / rackSlot" which 
prompts for these two fields and then modifies the selected device accordingly.  

The latter is another example of using a router ( Zenoss.remote.myAppRouter.myRouterFunc(opts, .....) 
to channel data from the GUI and a facade (myAppFacade) to actually change the attributes
of the object to the values that have been input. Both router and facade need entries in the
top-level configure.zcml and the facade also needs an entry in interfaces.py.

Adding extra items to a device's Action menu
---------------------------------------------

One can also add to the Action menu on the device details page.  A viewlet entry is required 
in browser/configure.zcml that points to the javascript file deviceGearMenu.js.  Note that the
manager field needs to be:

manager="Products.ZenUI3.browser.interfaces.IHeadExtraManager"

Two extra options have been added.  The first simply logs to a console log (which you could
see with the Firebug plugin).  The second option again runs the predefined command discussed
earlier.


General Comments
----------------
There are two configure.zcml files to provide the necessary "wiring" between objects and
layout.  In this ZenPack, most of the wiring is to do with the browser so the top-level
configure.zcml only has a few entries and a line to include the browser package:

<include package=".browser"/>

browser/configure.zcml defines a resources directory called example which points to the
resources subdirectory.

Download
========
Download the appropriate package for your Zenoss version from the list
below.

* Zenoss 3.0+ `Latest Package for Python 2.6`_
* Zenoss 4.0+ `Latest Package for Python 2.7`_

ZenPack installation
======================

This ZenPack can be installed from the .egg file using either the GUI or the
zenpack command line but, since it is demonstration code that you are likely to 
want to modify, it is more likely installed in development mode.  From github - 
https://github.com/jcurry/ZenPacks.skills1st.MenuExamples  use the ZIP button
(top left) to download a tgz file and unpack it to a local directory, say,
$ZENHOME/local.  Install from $ZENHOME/local with:

zenpack --link --install ZenPacks.skills1st.MenuExamples

Restart zenoss completely after installation.



Change History
==============
* 1.0
   * Initial Release
* 1.0.3
   * All menus now working
* 2.0
   * Tested with Zenoss Core 4.2

Screenshots
===========
|menus1|
|menus2|
|menus3|
|menus4|
|menus5|
|menus6|
|menus7|


.. External References Below. Nothing Below This Line Should Be Rendered

.. _Latest Package for Python 2.6: https://github.com/jcurry/ZenPacks.skills1st.MenuExamples/blob/master/dist/ZenPacks.skills1st.MenuExamples-1.0.3-py2.6.egg?raw=true
.. _Latest Package for Python 2.7: https://github.com/downloads/jcurry/ZenPacks.skills1st.MenuExamples/ZenPacks.skills1st.MenuExamples-2.0-py2.7.egg

.. |menus1| image:: http://github.com/jcurry/ZenPacks.skills1st.MenuExamples/raw/master/screenshots/menus1.jpg
.. |menus2| image:: http://github.com/jcurry/ZenPacks.skills1st.MenuExamples/raw/master/screenshots/menus2.jpg
.. |menus3| image:: http://github.com/jcurry/ZenPacks.skills1st.MenuExamples/raw/master/screenshots/menus3.jpg
.. |menus4| image:: http://github.com/jcurry/ZenPacks.skills1st.MenuExamples/raw/master/screenshots/menus4.jpg
.. |menus5| image:: http://github.com/jcurry/ZenPacks.skills1st.MenuExamples/raw/master/screenshots/menus5.jpg
.. |menus6| image:: http://github.com/jcurry/ZenPacks.skills1st.MenuExamples/raw/master/screenshots/menus6.jpg
.. |menus7| image:: http://github.com/jcurry/ZenPacks.skills1st.MenuExamples/raw/master/screenshots/menus7.jpg


Acknowledgements
================
Thanks are due to several people who have contributed either directly or indirectly to
this project:

Chet Luther for the original ZenPackTemplate ZenPack and for several good hints along the way.

Josh Goebel for help with the footer menus.

Joseph Hanson for lots of good hints and code samples.

Shane Scott for extra ZenPack samples.

j053ph4 on the Zenoss forum for various contributions.

phonegi from the Zenoss forum for lots of work figuring out component menus.

Kells Kearney for code snippets to run predefined commands.

Nick Yeates for bullying Zenoss engineers into helping!

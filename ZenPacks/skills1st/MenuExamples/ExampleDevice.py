from Products.ZenModel.Device import Device
from Products.ZenRelations.RelSchema import ToManyCont, ToOne
from copy import deepcopy
from AccessControl import Permissions


class ExampleDevice(Device):
    """
    Example device subclass. In this case the reason for creating a subclass of
    device is to add a new type of relation. We want many "ExampleComponent"
    components to be associated with each of these devices.

    If you set the zPythonClass of a device class to
    ZenPacks.NAMESPACE.PACKNAME.ExampleDevice, any devices created or moved
    into that device class will become this class and be able to contain
    ExampleComponents.
    """

    meta_type = portal_type = 'ExampleDevice'

    # This is where we extend the standard relationships of a device to add
    # our "exampleComponents" relationship that must be filled with components
    # of our custom "ExampleComponent" class.
    _relations = Device._relations + (
        ('exampleComponents', ToManyCont(ToOne,
            'ZenPacks.skills1st.MenuExamples.ExampleComponent',
            'exampleDevice',
            ),
        ),
    )

    # The menus for this particular device class will have all the standard menus
    # for a Device and then add on this new menu.  The "action" field specifies
    # the page template (.pt) file that defines the menu.

    factory_type_information = deepcopy(Device.factory_type_information)
    factory_type_information[0]['actions'] += (
            { 'id'              : 'ExampleDevice'
            , 'name'            : 'My Example Menu 2 (Example Devices only)'
            , 'action'          : 'myExampleMenuTwo'
            , 'permissions' 	: ( Permissions.view,) },
            )



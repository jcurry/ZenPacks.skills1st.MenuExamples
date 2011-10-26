from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity
from Products.ZenModel.ZenossSecurity import ZEN_CHANGE_DEVICE
from Products.ZenRelations.RelSchema import ToManyCont, ToOne


class ExampleComponent(DeviceComponent, ManagedEntity):
    meta_type = portal_type = "ExampleComponent"

    devDescr = None
    devStatus = None
    devErrors = None

    _properties = ManagedEntity._properties + (
        {'id': 'devDescr', 'type': 'string', 'mode': ''},
        {'id': 'devStatus', 'type': 'int', 'mode': ''},
        {'id': 'devErrors', 'type': 'int', 'mode': ''},
    )

    _relations = ManagedEntity._relations + (
        ('exampleDevice', ToOne(ToManyCont,
            'ZenPacks.skills1st.MenuExamples.ExampleDevice',
            'exampleComponents',
            ),
        ),
    )

    # Defining the "perfConf" action here causes "Example Component Template" to be available in
    # the display dropdown  for components of this type.
    # The action "objTemplates" is a standard Zenoss page template defined in
    #      /usr/local/zenoss/zenoss/Products/ZenModel/skins/zenmodel/objTemplates.pt

    factory_type_information = ({
        'actions': ({
            'id': 'perfConf',
            'name': 'Example Component Template',
            'action': 'objTemplates',
            'permissions': (ZEN_CHANGE_DEVICE,),
        },),
    },)

    # Custom components must always implement the device method. The method
    # should return the device object that contains the component.
    def device(self):
        return self.exampleDevice()



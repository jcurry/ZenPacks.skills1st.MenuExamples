from Products.Zuul.form import schema
from Products.Zuul.interfaces.component import IComponentInfo
from Products.Zuul.interfaces import IFacade


# ZuulMessageFactory is the translation layer. You will see strings intended to
# been seen in the web interface wrapped in _t(). This is so that these strings
# can be automatically translated to other languages.
from Products.Zuul.utils import ZuulMessageFactory as _t

# In Zenoss 3 we mistakenly mapped TextLine to Zope's multi-line text
# equivalent and Text to Zope's single-line text equivalent. This was
# backwards so we flipped their meanings in Zenoss 4. The following block of
# code allows the ZenPack to work properly in Zenoss 3 and 4.

# Until backwards compatibility with Zenoss 3 is no longer desired for your
# ZenPack it is recommended that you use "SingleLineText" and "MultiLineText"
# instead of schema.TextLine or schema.Text.
from Products.ZenModel.ZVersion import VERSION as ZENOSS_VERSION
from Products.ZenUtils.Version import Version
if Version.parse('Zenoss %s' % ZENOSS_VERSION) >= Version.parse('Zenoss 4'):
    SingleLineText = schema.TextLine
    MultiLineText = schema.Text
else:
    SingleLineText = schema.Text
    MultiLineText = schema.TextLine

class IExampleComponentInfo(IComponentInfo):
    """
    Info adapter for ExampleComponent
    """

    devDescr = SingleLineText(title=_t(u"Device Description"), readonly=True, group='Details')
    devStatus = schema.Int(title=_t(u"Device Status"), readonly=True, group='Details')
    devErrors = schema.Int(title=_t(u"Device Errors"), readonly=True, group='Details')

class IHardDiskInfo(IComponentInfo):
    """
    Info adapter for HardDisk
    """
    description = SingleLineText(title=_t(u"Hard Disk Description"), readonly=True, group='Details')

# The name of the IFacade class here ( IExampleDeviceFacade ) must match what is defined in an
#   adapter stanza's provides=".interfaces. this_is_the_bit_that_must_match"
#   ie. IExampleDeviceFacade in configure.zcml
# The method name and parameters must match those defined for the facade that implements
#   IExampleDeviceFacade in facades.py (ie. add_ExampleDevice )


class IExampleDeviceFacade(IFacade):
    def add_ExampleDevice(self, deviceIp, community, comment):
        """Add a device of class ExampleDevice"""

# The name of the IFacade class here ( IAppFacade ) must match what is defined in an
#   adapter stanza's provides=".interfaces. this_is_the_bit_that_must_match"
#   ie. IAppFacade in configure.zcml
# The method name and parameters must match those defined for the facade that implements
#   IAppFacade in facades.py (ie. myFacadeFunc )

class ImyAppFacade(IFacade):
    def myFacadeFunc(self, ob, comments, rackSlot):
        """ Modify comments / rackSlot attributes for a device object"""


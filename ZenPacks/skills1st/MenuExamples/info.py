# This file is the conventional place for "Info" adapters. Info adapters are
# a crucial part of the Zenoss API and therefore the web interface for any
# custom classes delivered by your ZenPack. Examples of custom classes that
# will almost certainly need info adapters include datasources, custom device
# classes and custom device component classes.

# Mappings of interfaces (interfaces.py) to concrete classes and the factory
# (these info adapter classes) used to create info objects for them are managed
# in the configure.zcml file.

from zope.component import adapts
from zope.interface import implements

from Products.Zuul.infos import ProxyProperty
from Products.Zuul.infos.component import ComponentInfo

from ZenPacks.skills1st.MenuExamples.ExampleComponent import ExampleComponent
from ZenPacks.skills1st.MenuExamples import interfaces
from Products.ZenModel.HardDisk import HardDisk


class ExampleComponentInfo(ComponentInfo):
    implements(interfaces.IExampleComponentInfo)
    adapts(ExampleComponent)

    devDescr = ProxyProperty("devDescr")
    devStatus = ProxyProperty("devStatus")
    devErrors = ProxyProperty("devErrors")

class HardDiskInfo(ComponentInfo):
    implements(interfaces.IHardDiskInfo)
    adapts(HardDisk)

    description = ProxyProperty("description")

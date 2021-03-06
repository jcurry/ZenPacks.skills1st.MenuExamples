# Module-level documentation will automatically be shown as additional
# information for the modeler plugin in the web interface.
"""
ExampleCMD
An example plugin that illustrates how to model devices using SSH.
"""

# This is an example of an CMD-based modeler plugin. It won't be recognized by
# Zenoss as an available modeler plugin unless the .example extension is
# removed.

# When configuring modeler plugins for a device or device class, this plugin's
# name would be community.cmd.ExampleCMD because its filesystem path within
# the ZenPack is modeler/plugins/community/cmd/ExampleCMD.py. The name of the
# class within this file must match the filename.

import re

# CommandPlugin is the base class that provides lots of help in modeling data
# that's available by connecting to a remote machine, running command line
# tools, and parsing their results.
from Products.DataCollector.plugins.CollectorPlugin import CommandPlugin

# Classes we'll need for returning proper results from our modeler plugin's
# process method.
from Products.DataCollector.plugins.DataMaps import ObjectMap, RelationshipMap


class ExampleCMD(CommandPlugin):

    # The command to run.
    command = "/bin/cat /proc/partitions"

    # Modeler plugins can optionally implement the "condition" method. This
    # allows your plugin to determine if it should be run by looking at the
    # configuration of the device that's about to be modeled. Return True if
    # you want the modeler plugin to execute and False if you do not.
    #
    # The default is to return True. So ordinarily you wouldn't even implement
    # the method if you were just going to blindly return True like this
    # example.
    def condition(self, device, log):
        return True

    def process(self, device, results, log):
        log.info("Modeler %s processing data for device %s",
            self.name(), device.id)

        objectmaps = []

        # For CommandPlugin, the results parameter to the process method will
        # be a string containing all output from the command defined above.

        # results contents..
        # major minor  #blocks  name
        #
        #    8     0   41943040 sda
        #    8     1     104391 sda1
        #    8     2   41833260 sda2
        #  253     0   41091072 dm-0
        #  253     1     720896 dm-1

        matcher = re.compile(r'^\d+\s+\d+\s+(?P<blocks>\d+)\s+(?P<name>\S+)')

        for line in results.split('\n'):
            line = line.strip()
            match = matcher.search(line)
            if match:
                objectmaps.append(ObjectMap({
                    'id': self.prepId(match.group('name')),
                    'description': match.group('name'),
                    }))

        # Return a RelationshipMap that describes the component, relationship
        # on that component, and the module name for the created objects. Pass
        # in the previously built list of ObjectMaps that will be used to
        # populate the relationship.
        return RelationshipMap(
            compname="hw", relname="harddisks",
            modname='Products.ZenModel.HardDisk',
            objmaps=objectmaps)

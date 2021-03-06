# Module-level documentation will automatically be shown as additional
# information for the modeler plugin in the web interface.
"""
ExampleSNMP
An example plugin that illustrates how to model devices using SNMP.
"""

# This is an example of an SNMP-based modeler plugin. It won't be recognized by
# Zenoss as an available modeler plugin unless the .example extension is
# removed.

# When configuring modeler plugins for a device or device class, this plugin's
# name would be community.snmp.ExampleSNMP because its filesystem path within
# the ZenPack is modeler/plugins/community/snmp/ExampleSNMP.py. The name of the
# class within this file must match the filename.

# SnmpPlugin is the base class that provides lots of help in modeling data
# that's available over SNMP.
from Products.DataCollector.plugins.CollectorPlugin \
    import SnmpPlugin, GetMap, GetTableMap

# Classes we'll need for returning proper results from our modeler plugin's
# process method.
from Products.DataCollector.plugins.DataMaps import ObjectMap


class ExampleSNMP(SnmpPlugin):

    # SnmpPlugin will automatically collect OIDs described in the snmpGetMap
    # property. You can make up the value for the OID key. It will be used in
    # the process method to find the result for each value. snmpGetMap and
    # GetMap should be used to request specific OIDs as you would in an
    # snmpget.
    snmpGetMap = GetMap({
        '.1.3.6.1.4.1.2021.4.3.0': 'memTotalSwap',
        '.1.3.6.1.4.1.2021.4.5.0': 'memTotalReal',
        })

    # snmpGetTableMaps and GetTableMap should be used to request SNMP tables.
    # The first parameter to GetTableMap is whatever you want the results of
    # this table to be stored in the results as. The second parameter is the
    # base OID for the table. More specifically this should be the "entry" OID
    # or more specifically the largest possible OID prefix that doesn't change
    # when walking the table. The third paramter is a dictionary that maps
    # columns in the table to names that will be used to access them in the
    # results.
    snmpGetTableMaps = (
        GetTableMap('diskIOTable', '.1.3.6.1.4.1.2021.13.15.1.1', {
            '.1': 'index',
            '.2': 'device',
            }),

        # More GetTableMap definitions can be added to this tuple to query
        # more SNMP tables.
        )

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

        # Results is a tuple with two items. The first (0) index contains a
        # dictionary with the results of our "snmpGetMap" queries. The second
        # (1) index contains a dictionary with the results of our
        # "snmpGetTableMaps" queries.
        getdata, tabledata = results

        # getdata contents..
        # {'memTotalReal': 2058776, 'memTotalSwap': 720888}

        # tabledata contents..
        # {'diskIOTable': {'1': {'device': 'ram0', 'index': 1},
        #                  '2': {'device': 'ram1', 'index': 2},
        #                  '3': {'device': 'ram2', 'index': 3},
        #                  '4': {'device': 'ram4', 'index': 4}}}

        # Create a list to fill up with our results.
        maps = []

        # First we build an ObjectMap to apply to the device's hardware (hw)
        # component to set the total memory size. Need to check whether SNMP value
        # suppilied for memTotalReal.  If so, multiply the returned value
        # by 1024 because the SNMP result is in kilybytes and we want to store
        # it in bytes.
        if getdata['memTotalReal']:
            maps.append(ObjectMap({
                'totalMemory': getdata['memTotalReal'] * 1024},
                compname='hw'))

        # Now do the same thing for total swap space. Zenoss stores this on the
        # Operating System (os) component of the device.
        if getdata['memTotalSwap']:
            maps.append(ObjectMap({
                'totalSwap': getdata['memTotalSwap'] * 1024},
                compname='os'))

        # Log for each disk returned from our GetTableMap. If we wanted to
        # create new disks in the model we'd create a RelationshipMap for them
        # and add an ObjectMap to it for each row in this table. See the
        # ExampleCMD plugin for an example of this.
        for snmpindex, disk in tabledata.get('diskIOTable').items():
            log.info("Found disk %s", disk['device'])

        # The process method of the modeler plugin class below is expected to
        # return output in one of the following forms.
        #
        #   1. A single ObjectMap instance
        #   2. A single RelationshipMap instance
        #   3. A list of ObjectMap and RelationshipMap instances
        #   4. None
        #
        # If your modeler plugin encounters a bad state and you don't want to
        # affect Zenoss' model of the device you should return None.
        return maps

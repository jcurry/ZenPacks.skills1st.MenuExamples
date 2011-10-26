# Module-level documentation will automatically be shown as additional
# information for the modeler plugin in the web interface.
"""
ExampleHostResourcesSNMP
An example plugin that illustrates how to model devices using SNMP to get host resources device info.
"""

# When configuring modeler plugins for a device or device class, this plugin's
# name would be community.snmp.ExampleHostResourcesSNMP because its filesystem path within
# the ZenPack is modeler/plugins/community/snmp/ExampleHostResourcesSNMP.py. The name of the
# class within this file must match the filename.

# SnmpPlugin is the base class that provides lots of help in modeling data
# that's available over SNMP.
from Products.DataCollector.plugins.CollectorPlugin \
    import SnmpPlugin, GetMap, GetTableMap

# Classes we'll need for returning proper results from our modeler plugin's
# process method.
from Products.DataCollector.plugins.DataMaps import ObjectMap


class ExampleHostResourcesSNMP(SnmpPlugin):

#
# The modname is ZenPacks.<org name>.<ZenPack name>.<component class name>
# relname is the relationship on the device that you want to populate
#
    maptype = 'ExampleHostResourcesSNMP'
    modname = "ZenPacks.skills1st.MenuExamples.ExampleComponent"
    relname = 'exampleComponents'

    # snmpGetTableMaps and GetTableMap should be used to request SNMP tables.
    # The first parameter to GetTableMap is whatever you want the results of
    # this table to be stored in the results as. The second parameter is the
    # base OID for the table. More specifically this should be the "entry" OID
    # or more specifically the largest possible OID prefix that doesn't change
    # when walking the table. The third paramter is a dictionary that maps
    # columns in the table to names that will be used to access them in the
    # results.
    snmpGetTableMaps = (

        GetTableMap('hrDevice', '.1.3.6.1.2.1.25.3.2.1', {
            '.1': '_index',
            '.3': 'devDescr',
            '.5': 'devStatus',
            '.6': 'devErrors',
            }),
        )

        # More GetTableMap definitions can be added to this tuple to query
        # more SNMP tables.

    def process(self, device, results, log):
        log.info("Modeler %s processing data for device %s",
            self.name(), device.id)

        # Results is a tuple with two items. The first (0) index contains a
        # dictionary with the results of our "snmpGetMap" queries. The second
        # (1) index contains a dictionary with the results of our
        # "snmpGetTableMaps" queries.
        getdata, tabledata = results

        # tabledata contents..
        # Note that for this particulat set of table data, some OIDs do not
        #   return values eg. errors and status.  Although this is unfortunate
        #   for the code, it is by no means uncommon with SNMP.
        #   This is why the main body of the loop is a try / except clause and the
        #     except will print warning messages when an ExampleComponent cannot be
        #     instantiated because of this missing data
        #   
        # 'hrDevice': 
        #      status  {'.1.3.6.1.2.1.25.3.2.1.5': {'.1.3.6.1.2.1.25.3.2.1.5.1028': 2, 
        #                                           '.1.3.6.1.2.1.25.3.2.1.5.1025': 2, 
        #                                           '.1.3.6.1.2.1.25.3.2.1.5.1027': 5, 
        #                                           '.1.3.6.1.2.1.25.3.2.1.5.768': 2, 
        #                                           '.1.3.6.1.2.1.25.3.2.1.5.1026': 5}, 
        #      errors   '.1.3.6.1.2.1.25.3.2.1.6': {'.1.3.6.1.2.1.25.3.2.1.6.1025': 0L, 
        #                                            '.1.3.6.1.2.1.25.3.2.1.6.1026': 0L, 
        #                                             '.1.3.6.1.2.1.25.3.2.1.6.1027': 0L, 
        #                                             '.1.3.6.1.2.1.25.3.2.1.6.1028': 160L}, 
        #      index    '.1.3.6.1.2.1.25.3.2.1.1': {'.1.3.6.1.2.1.25.3.2.1.1.1552': 1552, 
        #                                           '.1.3.6.1.2.1.25.3.2.1.1.1028': 1028, 
        #                                           '.1.3.6.1.2.1.25.3.2.1.1.1025': 1025, 
        #                                           '.1.3.6.1.2.1.25.3.2.1.1.768': 768, 
        #                                           '.1.3.6.1.2.1.25.3.2.1.1.1026': 1026, 
        #                                           '.1.3.6.1.2.1.25.3.2.1.1.3072': 3072, 
        #                                           '.1.3.6.1.2.1.25.3.2.1.1.1027': 1027}, 
        #      descr    '.1.3.6.1.2.1.25.3.2.1.3': {'.1.3.6.1.2.1.25.3.2.1.3.1027': 'network interface irda0', 
        #                                           '.1.3.6.1.2.1.25.3.2.1.3.1026': 'network interface eth0', 
        #                                           '.1.3.6.1.2.1.25.3.2.1.3.1025': 'network interface lo', 
        #                                           '.1.3.6.1.2.1.25.3.2.1.3.3072': "Guessing that there's a floating point co-processor", 
        #                                           '.1.3.6.1.2.1.25.3.2.1.3.768': 'GenuineIntel: Intel(R) Pentium(R) M processor 1.60GHz', 
        #                                           '.1.3.6.1.2.1.25.3.2.1.3.1552': 'SCSI disk (/dev/sda)', 
        #                                           '.1.3.6.1.2.1.25.3.2.1.3.1028': 'network interface eth1'}}
        #               }

        # Create a list to fill up with our results.

        # Check that we did get an SNMP response.  If not, get out of here.

        hrDeviceTable = tabledata.get('hrDevice')
        if not hrDeviceTable:
            log.warn( 'No SNMP response from %s for the %s plugin for hrDevice:', device.id, self.name() )
            log.warn( "Data= %s", tabledata )
            return

        # Main body

        rm=self.relMap()
        for oid, data in hrDeviceTable.items():
            try:
                om=self.objectMap(data)
                om.snmpindex = oid.strip('.')
        #
        # You MUST have an om.id or you will get modeler errors eg.
        #          ERROR zen.Events: (1054, "Unknown column 'None' in 'field list'")
        #
                om.id = self.prepId( om.snmpindex.replace('.','_') )
                log.info( ' devDescr is %s  devStatus is %s  devErrors is %s oid is %s  id is %s  ' % (om.devDescr, om.devStatus, om.devErrors, om.snmpindex, om.id))
                rm.append(om)
            except (KeyError, IndexError, AttributeError, TypeError), errorInfo:
                log.warn( ' Error in %s modeler plugin %s' % ( self.name(), errorInfo))
                continue
        return rm

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

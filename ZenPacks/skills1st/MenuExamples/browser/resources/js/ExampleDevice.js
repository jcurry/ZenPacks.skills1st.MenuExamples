/*
 * Based on the configuration in ../../configure.zcml this JavaScript will only
 * be loaded when the user is looking at an ExampleDevice in the web interface.
 */

(function(){

var ZC = Ext.ns('Zenoss.component');

/*
 * Custom component grid panel. This controls the grid that gets displayed for
 * components of the type set in "componentType".
 *
 * The name of the component panel MUST be the exact name of the object component
 *    catenated with Panel - hence ExampleComponentPanel
 *
 * Any columns that use a "dataIndex", that dataIndex name must appear in the fields stanza
 *    but order is NOT important. You must include uid in the fields stanza (but need not include in columns).
 *    If you do NOT include "monitor" in the fields stanza, then there will be no Graphs
 *        option in the DISPLAY dropdown.
 * It is the order of the stanzas under "columns" that defines the order on the web page
 *
 * Use the Zenoss-provided ping status renderer to display icons for devStatus where
 *      status=2 = running = green,   otherwise red
 */
ZC.ExampleComponentPanel = Ext.extend(ZC.ComponentGridPanel, {
    subComponentGridPanel: false,

    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            autoExpandColumn: 'name',
            componentType: 'ExampleComponent',
            sortInfo: {
                field: 'name',
                direction: 'ASC'
            },
            fields: [
                {name: 'uid'},
                {name: 'name'},
                {name: 'severity'},
                {name: 'monitor'},
                {name: 'devDescr'},
                {name: 'devStatus'},
                {name: 'devErrors'}
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                sortable: true,
                width: 50
            },{
                id: 'devDescr',
                dataIndex: 'devDescr',
                header: _t('Device description'),
                sortable: true,
                width: 200
            },{
                id: 'devStatus',
                dataIndex: 'devStatus',
                header: _t('Device Status'),
                renderer: function(dS) {
                        if (dS==2) {
                          return Zenoss.render.pingStatus('up');
                        } else {
                          return Zenoss.render.pingStatus('down');
                        }
                },
                sortable: true,
                width: 100
            },{
                id: 'devErrors',
                dataIndex: 'devErrors',
                header: _t('Device Errors'),
                sortable: true,
                width: 150
            },{
                id: 'name',
                dataIndex: 'name',
                header: _t('Name'),
                sortable: true,
                width: 70
            }]
        });
        ZC.ExampleComponentPanel.superclass.constructor.call(this, config);
    }
});


Ext.reg('ExampleComponentPanel', ZC.ExampleComponentPanel);
/*
 * Friendly names for the components. First parameter is the meta_type in your
 * custom component class. Second parameter is the singular form of the
 * friendly name to be displayed in the UI. Third parameter is the plural form.
 */
ZC.registerName('ExampleComponent', _t('Example Component'), _t('Example Components'));

ZC.HardDiskPanel = Ext.extend(ZC.ComponentGridPanel, {
    subComponentGridPanel: false,

    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            autoExpandColumn: 'name',
            componentType: 'HardDisk',
            sortInfo: {
                field: 'name',
                direction: 'ASC'
            },
            fields: [
                {name: 'uid'},
                {name: 'name'},
                {name: 'severity'},
                {name: 'monitor'},
                {name: 'description'}
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                sortable: true,
                width: 50
            },{
                id: 'description',
                dataIndex: 'description',
                header: _t('Hard Disk Description'),
                sortable: true,
                width: 150
            },{
                id: 'name',
                dataIndex: 'name',
                header: _t('Name'),
                sortable: true,
                width: 70
            }]
        });
        ZC.HardDiskPanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('HardDiskPanel', ZC.HardDiskPanel);
/*
 * Friendly names for the components. First parameter is the meta_type in your
 * custom component class. Second parameter is the singular form of the
 * friendly name to be displayed in the UI. Third parameter is the plural form.
 */
ZC.registerName('HardDisk', _t('Hard Disk'), _t('Hard Disks'));


})();

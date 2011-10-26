/*
 * Based on the configuration in ../../configure.zcml this JavaScript will only
 * be loaded when the user is looking at an ExampleDevice in the web interface.
 */

(function(){

var ZC = Ext.ns('Zenoss.component');

/*
 * Custom component grid panel. This controls the grid that gets displayed for
 * components of the type set in "componenType".
 */
ZC.ExampleComponentGridPanel = Ext.extend(ZC.ComponentGridPanel, {
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
                {name: 'devDescr'},
                {name: 'devStatus'},
                {name: 'devErrors'},
                {name: 'monitor'},
                {name: 'monitored'}
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
                sortable: true,
                width: 100
            },{
                id: 'devErrors',
                dataIndex: 'devErrors',
                header: _t('Device Errors'),
                sortable: true,
                width: 150
            },{
                id: 'monitored',
                dataIndex: 'monitored',
                header: _t('Monitored'),
                renderer: Zenoss.render.checkbox,
                sortable: true,
                width: 65
            },{
                id: 'name',
                dataIndex: 'name',
                header: _t('Name'),
                width: 150
            }]
        });
        ZC.ExampleComponentGridPanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('ExampleComponentGridPanel', ZC.ExampleComponentGridPanel);
/*
 * Friendly names for the components. First parameter is the meta_type in your
 * custom component class. Second parameter is the singular form of the
 * friendly name to be displayed in the UI. Third parameter is the plural form.
 */
ZC.registerName('ExampleComponent', _t('Example Component'), _t('Example Components'));


})();

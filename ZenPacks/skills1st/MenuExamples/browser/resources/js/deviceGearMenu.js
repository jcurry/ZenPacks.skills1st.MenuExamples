(function() {

/**
* On the device details page the uid is
* Zenoss.env.device_uid and on most other pages it is set with
* the environmental variable PARENT_CONTEXT;
**/
    function getPageContext() {
        return Zenoss.env.device_uid || Zenoss.env.PARENT_CONTEXT;
    }

    Ext.ComponentMgr.onAvailable('device_configure_menu', function(config) {
        var menuButton = Ext.getCmp('device_configure_menu');
        menuButton.menuItems.push({
            xtype: 'menuitem',
            text: _t('Example Device Action'),
            handler: function(){
                console.log('JC - example device action clicked!');
            }
          },{
            xtype: 'menuitem',
            text: _t(' Another example device action'),
            handler: function() {
                var win = new Zenoss.CommandWindow({
                    uids: getPageContext(),
                    target: 'run_my_predefined_command',
                    title: _t('Janes Title in device Action menu window')
                });
                win.show();
            }
        });

    });
}());



// New menu option on the device list cog wheel menu, context-configure-menu

Ext.ComponentMgr.onAvailable('context-configure-menu', function(config) {
  var origOnGet = config.onGetMenuItems;
  config.onGetMenuItems = function(uid) {
    var result = origOnGet.call(this, uid) || [];
    // Menu item only shows up when certain device class is selected
//    if( uid.match('^/zport/dmd/Devices/Example/TestClass/') ) {
    if( true ) {
        result.push( {
            text: _t('Run My Predefined Shell Command'),
            hidden: Zenoss.Security.doesNotHavePermission('Manage Device'),
            handler: function() {
                var win = new Zenoss.CommandWindow({
                    uids: uid,
                    target: 'run_my_predefined_command',
                    title: _t('Janes Title in window')
                });
                win.show();
            }
        });
    }
    return result;
  };
});



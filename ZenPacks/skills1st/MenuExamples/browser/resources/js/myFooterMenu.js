(function(){

    /**
* On the device details page the uid is
* Zenoss.env.device_uid and on most other pages it is set with
* the environmental variable PARENT_CONTEXT;
**/
    function getPageContext() {
        return Zenoss.env.device_uid || Zenoss.env.PARENT_CONTEXT;
    }

    // whenever the footer bar is available we want to add a button
    Ext.ComponentMgr.onAvailable('footer_bar', function(config) {
        var footer_bar = Ext.getCmp('footer_bar');
        // the component is built but it is not ready for items to
        // be added so add a listener for after it is rendered
        footer_bar.on('render', function(){

            // add our menu items
            footer_bar.add([{
                text: 'MyFooter',
                id: 'my-footer-bar-menu',
                menu: {
                    items: [{
                        xtype: 'menuitem',
                        text: _t('Model Device') + '...',
                        hidden: Zenoss.Security.doesNotHavePermission('Manage Device'),
                        handler: function() {
                            var win = new Zenoss.CommandWindow({
                                uids: [getPageContext()],
                                target: 'run_model',
                                title: _t('Model Device')
                            });
                            win.show();
                        }
                    },{
                        xtype: 'menuitem',
                        text: 'Jane\'s predefined command',
                        handler: function() {
                            var win = new Zenoss.CommandWindow({
                                uids: getPageContext(),
                                target: 'run_my_predefined_command',
                                title: _t('Janes Title in footer_bar window')
                            });
                            win.show();
                        }
                    }]
                }
            }]);
        }, footer_bar, {single: true});
    });

}());



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
                        text: _t('Set device comment / rackSlot') + '...',
                        hidden: Zenoss.Security.doesNotHavePermission('Manage Device'),
                        handler: function() {
                            var win = new Zenoss.dialog.CloseDialog({
                                width: 300,
                                title: _t('Modify comment / rackSlot'),
                                items: [{
                                    xtype: 'form',
                                    buttonAlign: 'left',
                                    monitorValid: true,
                                    labelAlign: 'top',
                                    footerStyle: 'padding-left: 0',
                                    border: false,
                                    // Ensure that name field of items match the attribute names
                                    //   that you want to populate
                                    // allowBlank: false means OK button will not be active until this condition satisfied
                                    //  if allowBlank set to true and field not supplied then field will be set to null
                                    items: [{
                                        xtype: 'textfield',
                                        name: 'comments',
                                        fieldLabel: _t('Comments for device'),
                                        id: "exampleDeviceCommentField",
                                        width: 260,
                                        allowBlank: true
                                    }, {
                                        xtype: 'textfield',
                                        name: 'rackSlot',
                                        fieldLabel: _t('Rack Slot for this device'),
                                        id: "exampleDeviceRackSlotField",
                                        width: 260,
                                        allowBlank: false
                                    }],
                                    buttons: [{
                                        xtype: 'DialogButton',
                                        id: 'modifyExampleDevice-submit',
                                        text: _t('Modify'),
                                        formBind: true,
                                        handler: function(b) {
                                            var form = b.ownerCt.ownerCt.getForm();
                                            var opts = form.getFieldValues();
                    
                                            //  Following line must match the class defined in routers.py
                                            //    and the last part must match the method defined on that class
                                            //    ie. router class = myAppRouter, method = myRouterFunc
                                            //    The 2 input fields for comments and rackSlot are passed as
                                            //       opts to the router function.
                    
                                            Zenoss.remote.myAppRouter.myRouterFunc(opts,
                                            function(response) {
                                                if (response.success) {
                                                    new Zenoss.dialog.SimpleMessageDialog({
                                                        title: _t(' Device modified'),
                                                        message: response.msg,
                                                        buttons: [{
                                                            xtype: 'DialogButton',
                                                            text: _t('OK')
                                                        }]
                                                    }).show();
                                                }
                                                else {
                                                    new Zenoss.dialog.SimpleMessageDialog({
                                                        message: response.msg,
                                                        buttons: [{
                                                            xtype: 'DialogButton',
                                                            text: _t('OK')
                                                        }]
                                                    }).show();
                                                }
                                            });
                                        }
                                    }, Zenoss.dialog.CANCEL]
                                }]
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



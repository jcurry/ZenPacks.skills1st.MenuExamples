(function(){

// Ensure that the following var name matches the method defined in
//   interfaces.py, routers.py and facades.py
// Also ensure the var name matches with the Zenoss.extensions.adddevice.push statement
//   at the end of this file

var myVar = new Zenoss.Action({
    text: _t('Modify Example Device comment / rackSlot') + '...',
    id: 'modifyExampleDevice-item',
    permission: 'Manage DMD',
    handler: function(btn, e){
        var win = new Zenoss.dialog.CloseDialog({
            width: 300,
            title: _t('Modify Example Device comment / rackSlot'),
            items: [{
                xtype: 'form',
                buttonAlign: 'left',
                monitorValid: true,
                labelAlign: 'top',
                footerStyle: 'padding-left: 0',
                border: false,
                // Ensure that name field of items match the attribute names
                //   that you want to populate
                items: [{
                    xtype: 'textfield',
                    name: 'comments',
                    fieldLabel: _t('Comments for device'),
                    id: "exampleDeviceCommentField",
                    width: 260,
                    allowBlank: false
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
                        //    ie. router class = myAppRouter, method = myVar

                        Zenoss.remote.myAppRouter.myVar(opts,
                        function(response) {
                            if (response.success) {
                                new Zenoss.dialog.SimpleMessageDialog({
                                    message: _t('Device modified'),
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
});

                                                                
// DON'T lose the closing bracket sets - you need                    
//   }());
// If you lose these nothing works and you get no error messages or warnings

}());

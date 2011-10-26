(function(){

// Ensure that the following var name matches the method defined in
//   interfaces.py, routers.py and facades.py
// Also ensure the var name matches with the Zenoss.extensions.adddevice.push statement
//   at the end of this file

var add_ExampleDevice = new Zenoss.Action({
    text: _t('Add Example Device') + '...',
    id: 'addExampleDevice-item',
    permission: 'Manage DMD',
    handler: function(btn, e){
        var win = new Zenoss.dialog.CloseDialog({
            width: 300,
            title: _t('Add Example Device'),
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
                    name: 'deviceIp',
                    fieldLabel: _t('Hostname or IP'),
                    id: "exampleDeviceTitleField",
                    width: 260,
                    allowBlank: false
                }, {
                    xtype: 'textfield',
                    name: 'community',
                    fieldLabel: _t('RO Community'),
                    id: "exampleDeviceRoCommunityField",
                    width: 260,
                    allowBlank: false
                }, {
                    xtype: 'textfield',
                    name: 'comment',
                    fieldLabel: _t('comment'),
                    id: "exampleDeviceCommentField",
                    width: 260,
                    allowBlank: true
                }],
                buttons: [{
                    xtype: 'DialogButton',
                    id: 'addExampleDevice-submit',
                    text: _t('Add'),
                    formBind: true,
                    handler: function(b) {
                        var form = b.ownerCt.ownerCt.getForm();
                        var opts = form.getFieldValues();

                        //  Following line must match the class defined in routers.py
                        //    and the last part must match the method defined on that class
                        //    ie. router class = ExampleDeviceRouter, method = add_ExampleDevice

                        Zenoss.remote.ExampleDeviceRouter.add_ExampleDevice(opts,
                        function(response) {
                            if (response.success) {
                                new Zenoss.dialog.SimpleMessageDialog({
                                    message: _t('Add Example Device job submitted.'),
                                    buttons: [{
                                        xtype: 'DialogButton',
                                        text: _t('OK')
                                    }, {
                                        xtype: 'button',
                                        text: _t('View Job Log'),
                                        handler: function() {
                                            window.location =
                                                '/zport/dmd/JobManager/jobs/' +
                                                response.jobId + '/viewlog';
                                        }
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

Ext.ns('Zenoss.extensions');
Zenoss.extensions.adddevice = Zenoss.extensions.adddevice instanceof Array ?
                              Zenoss.extensions.adddevice : [];
// Ensure the parameter in the next line (add_ExampleDevice) matches the var name at the top of the file

Zenoss.extensions.adddevice.push(add_ExampleDevice);
                                                                
// DON'T lose the closing bracket sets - you need                    
//   }());
// If you lose these nothing works and you get no error messages or warnings

}());

Ext.ComponentMgr.onAvailable('footer_bar', function(config) {
        var footer_bar = Ext.getCmp('footer_bar');
                footer_bar.add([{
                        xtype: 'button',
                        text: 'MyFooter',
                        handler: function(button) {
                            alert('got here');
                            }
                }]);

        footer_bar.add('-');
    });

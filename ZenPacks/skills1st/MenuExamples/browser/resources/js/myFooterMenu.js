Ext.ComponentMgr.onAvailable('footer_bar', function(config) {
  var footer_bar = Ext.getCmp('footer_bar');
           footer_bar.add([{
                        xtype: 'ContextConfigureMenu',
                        text: 'MyFooter',
                        id: 'my-footer-bar-menu',
                        listeners: {
                            render: function(){
                                this.setContext(UID);
                            }
                        },
                        menuItems: [{
                            xtype: 'menuitem',
                            text: _t('Model Device') + '...',
                            hidden: Zenoss.Security.doesNotHavePermission('Manage Device'),
                            handler: function() {
                                var win = new Zenoss.CommandWindow({
                                    uids: [UID],
                                    target: 'run_model',
                                    title: _t('Model Device')
                                });
                                win.show();
                            }
                        }]
                }]);

    });


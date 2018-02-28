odoo.define('postit.systray', function (require) {
"use strict";

var core = require('web.core');
var SystrayMenu = require('web.SystrayMenu');
var session = require('web.session');
var Widget = require('web.Widget');

var PostitItem = Widget.extend({
    template:'postit_systray_menu.PostitItem',
    events: {
        "click": "on_click",
    },

    start: function () {
        return this._super();
    },

    on_click: function (event) {
        event.preventDefault();
        var self = this;

        self.trigger_up('hide_app_switcher');
        self.do_action('prisme_postit.action_prisme_postit', {clear_breadcrumbs: true})      
    },

});

SystrayMenu.Items.push(PostitItem);

});

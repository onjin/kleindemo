/*global EventSource */

kleindemo = (function ($) {
    "use strict";

    var handleMessage = function (message) {
        // console.log(message.data);
    };

    var sendMove = function (x, y) {
        return $.post('move', {
            player: kleindemo.id,
            x: x,
            y: y
        });
    };

    var generateRandomID = function () {
        var id = '';
        for (var i = 32; i > 0; i--) {
            id += Math.floor(Math.random() * 16).toString(16);
        }
        return id;
    };

    var main = function () {
        var source = new EventSource('events');
        source.addEventListener('message', handleMessage);
    };

    return {
        id: generateRandomID(),
        main: main,
        sendMove: sendMove
    };
}(jQuery));

jQuery(document).ready(kleindemo.main);

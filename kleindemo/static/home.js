
kleindemo = (function () {
    "use strict";

    var handleMessage = function (message) {
        console.log(message.data);
    }
    
    var main = function () {
        var source = new EventSource('events');
        source.addEventListener('message', handleMessage);
    };

    return {main: main};
}());

jQuery(document).ready(kleindemo.main);

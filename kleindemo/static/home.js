/*global EventSource */

kleindemo = (function ($) {
    "use strict";

    var AVATAR_WIDTH = 80, AVATAR_HEIGHT = 80;

    var fieldSize = {width: null, height: null};

    var players = {};

    var newPlayer = function (playerID) {
        var $player = $('<img />', {
            'class': 'player',
            id: 'player-' + playerID,
            src: 'http://www.gravatar.com/avatar/' + playerID + '?d=monsterid'
        });
        if (playerID === kleindemo.id) {
            $player.addClass('you');
        }
        $player.appendTo('#playingField').css({'position': 'absolute'});
        players[playerID] = $player;
        return $player;
    };

    var receiveMove = function (jsonmsg) {
        var msg = $.parseJSON(jsonmsg.data);

        var playerID = msg.player;
        var $player = players[playerID];
        if (!$player) {
            $player = newPlayer(playerID);
        }
        var centerX = msg.x * fieldSize.width;
        var centerY = msg.y * fieldSize.height;

        $player.stop(true);
        $player.animate({
            left: centerX - AVATAR_WIDTH / 2,
            top: centerY - AVATAR_HEIGHT / 2
        }, 'fast');
    };

    var sendMove = function (x, y) {
        return $.post('move', {
            player: kleindemo.id,
            x: x,
            y: y
        });
    };


    /* from http://stackoverflow.com/a/5158301/9585 */
    function getParameterByName(name) {
        var match = new RegExp('[?&]' + name + '=([^&]*)')
            .exec(window.location.search);
        return match && decodeURIComponent(match[1].replace(/\+/g, ' '));
    }

    var generateRandomID = function () {
        var id = '';
        for (var i = 32; i > 0; i--) {
            id += Math.floor(Math.random() * 16).toString(16);
        }
        return id;
    };

    var myID = function () {
        return getParameterByName('id') || generateRandomID();
    };

    var handleClick = function (evt) {
        return sendMove(evt.pageX / fieldSize.width, evt.pageY / fieldSize.height);
    };

    var main = function () {
        var source = new EventSource('events');
        source.addEventListener('move', receiveMove);

        // For debugging when these event connections open and close.
        if (window.console) {
            source.addEventListener('open', function (m) {console.log(m)});
            source.addEventListener('error', function (m) {console.log(m)});
        }

        var $playingField = $("#playingField");
        $playingField.click(handleClick);
        fieldSize.width = $playingField.width();
        fieldSize.height = $playingField.height();
    };

    return {
        id: myID(),
        main: main,
        sendMove: sendMove
    };
}(jQuery));

jQuery(document).ready(kleindemo.main);

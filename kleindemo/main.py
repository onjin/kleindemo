import json
from klein import route
from twisted.python.util import sibpath
from twisted.web.static import File
from twisted.internet import defer

STATIC_DIR = sibpath(__file__, 'static/')

spectators = set()


@route('/static/')
def static(request):
    """All requests to /static/* are static files from this directory."""
    return File(STATIC_DIR)



@route('/')
def home(request):
    """A simple homepage."""
    with file(STATIC_DIR + 'home.html') as f:
        return f.read()



@route('/events')
def events(request):
    """Events will be sent on this channel as they happen.

    Uses the Server Sent Events protocol.
    """
    request.setHeader('Content-type', 'text/event-stream')

    # When we're running under heroku, it likes to know we've received the
    # request and aren't falling asleep on the job, so write something out
    # immediately.
    request.write(sseMsg('hello', 'keepalive'))

    # We'll want to write more things to this client later, so keep the request
    # around somewhere.
    spectators.add(request)

    # Indicate we're not done with this request by returning a deferred.
    # (In fact, this deferred will never fire, which is kinda fishy of us.)
    return defer.Deferred()



@route('/move')
def move(request):
    """Inform the server of a move.

    Expects three arguments:

    - player: 32-character player ID
    - x, y: coordinates (floats, 0.0 - 1.0)

    :type request: twisted.web.http.Request
    """
    player = request.args['player'][0]
    x = float(request.args['x'][0])
    y = float(request.args['y'][0])

    dropouts = []
    for spectator in spectators:
        if not spectator.transport.disconnected:
            spectator.write(sseMsg({'player': player, 'x': x, 'y': y}, "move"))
        else:
            # can't change spectators while we're iterating over it
            dropouts.append(spectator)

    for dropout in dropouts:
        spectators.remove(dropout)



def sseMsg(data, name=None):
    """Format a Sever-Sent-Event message.

    :param data: message data, will be JSON-encoded.

    :param name: (optional) name of the event type.

    :rtype: str
    """
    # We need to serialize the message data to a string.  SSE doesn't say that
    # we must use JSON for that, but it's a convenient choice.
    jsonData = json.dumps(data)

    # Newlines make SSE messages slightly more complicated.  Fortunately for us,
    # we don't have any in the messages we're using.
    assert '\n' not in jsonData

    if name:
        output = 'event: %s\n' % (name,)
    else:
        output = ''

    output += 'data: %s\n\n' % (jsonData,)
    return output


# Klein offers two helpers to start your server.  You really ought to
# pick one or the other of these, but I'm including both here for
# demonstration purposes.

if __name__ == '__main__':
    # For the simplest cases, you can use klein.run to start a web
    # server as soon as your script loads.
    from klein import run
    import os
    # Get the server port from the environment, or use default.
    port = int(os.environ.get('PORT', '8081'))

    # You tell it which network interface to listen on.  The empty string
    # '' will use all available interfaces.
    run('', port)

else:
    # klein.resource is a web.Resource you can use to refer to your
    # application from other Python modules, or used when starting
    # a server from the command line with twistd, like this:
    #
    # twistd -n web --class=kleindemo.main.resource
    #
    # twistd has an assortment of options for log files and
    # process management and other such useful things.

    #noinspection PyUnresolvedReferences
    from klein import resource

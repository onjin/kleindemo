import json
from klein import run, route
from twisted.python.util import sibpath
from twisted.web.static import File
from twisted.internet import defer

STATIC_DIR = sibpath(__file__, 'static/')

spectators = set()

@route('/static/')
def static(request):
    return File(STATIC_DIR)



@route('/')
def home(request):
    with file(STATIC_DIR + 'home.html') as f:
        return f.read()



@route('/events')
def events(request):
    request.setHeader('Content-type', 'text/event-stream')
    spectators.add(request)
    # Indicate we're not done with this request by returning a deferred.
    # (In fact, this deferred will never fire.)
    return defer.Deferred()



@route('/move')
def move(request):
    """

    :type request: twisted.web.http.Request
    """
    player = request.args['player'][0]
    x = float(request.args['x'][0])
    y = float(request.args['y'][0])

    dropouts = []
    for spectator in spectators:
        if not spectator.transport.disconnected:
            spectator.write(sseMsg({'player': player, 'x': x, 'y': y}))
        else:
            # can't change spectators while we're iterating over it
            dropouts.append(spectator)

    for dropout in dropouts:
        spectators.remove(dropout)



def sseMsg(data):
    """Format a Sever-Sent-Event message."""
    jsonData = json.dumps(data)
    # It's possible to deal with newlines in data, but we don't have to yet.
    assert '\n' not in jsonData
    return 'data: %s\n\n' % (jsonData,)



if __name__ == '__main__':
    import os
    port = os.environ.get('VCAP_APP_PORT', '8081')
    run('', int(port))
else:
    #noinspection PyUnresolvedReferences
    from klein import resource
    # now invoke server like this:
    # twistd -n web --class=kleindemo.main.resource

from klein import run, route
from twisted.web.static import File
from twisted.internet import defer, reactor


@route('/static/')
def static(request):
    return File("./static")



@route('/')
def home(request):
    with file('./static/home.html') as f:
        return f.read()



@route('/events')
def events(request):
    request.setHeader('Content-type', 'text/event-stream')
    ticker(request)
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
    print "%s moving to %r, %r" % (player, x, y)



def ticker(request, n=0):
    """Send a tick event and schedule the next tick.

    (As long as the request is connected.)
    """
    if not request.transport.disconnected:
        request.write('data: Tick %s\n\n' % (n,))
        reactor.callLater(1, ticker, request, n+1)    


if __name__ == '__main__':
    run("localhost", 8081)

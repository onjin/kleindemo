from klein import run, route
from twisted.web.static import File

@route('/static/')
def static(request):
    return File("./static")



@route('/')
def home(request):
    with file('./static/home.html') as f:
        return f.read()



if __name__ == '__main__':
    run("localhost", 8081)

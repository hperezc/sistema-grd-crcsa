from werkzeug.middleware.dispatcher import DispatcherMiddleware
from descriptores_app import app

# Mount Flask app under /autodiagnostico_GR prefix
app.config['APPLICATION_ROOT'] = '/autodiagnostico_GR'
application = DispatcherMiddleware(None, {
    '/autodiagnostico_GR': app
})

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('0.0.0.0', 8001, application)

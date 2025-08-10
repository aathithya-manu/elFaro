import serverless_wsgi
import app

def handler(event, context):
    return serverless_wsgi.handle(app, event, context)

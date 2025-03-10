import os
import time

from src_backend import createApp

# set global timezone to UTC
os.environ["TZ"] = "UTC"
time.tzset()

app = createApp()


@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = 'http://127.0.0.1:3000'
    response.headers['Access-Control-Allow-Headers'] = 'Authorization, Content-Type'
    response.headers['Access-Control-Expose-Headers'] = 'Authorization, DiscordId'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS, PUT, DELETE'

    return response


if __name__ == '__main__':
    # ssl_context = ('./certs/localhost.pem', './certs/localhost-key.pem')
    app.run(debug=not app.config["PRODUCTION"], host='0.0.0.0', port=8000) #, ssl_context=ssl_context)

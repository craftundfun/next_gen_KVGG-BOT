import os
import time

from src_backend import createApp

# set global timezone to UTC
os.environ["TZ"] = "UTC"
time.tzset()

app = createApp()

@app.after_request
def apply_cors(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS, PUT, DELETE"
    return response


# development only
if __name__ == '__main__':
    app.run(debug=not app.config["PRODUCTION"], host='0.0.0.0', port=8000)

import os
import time

from src_backend import createApp

# set global timezone to UTC
os.environ["TZ"] = "UTC"
time.tzset()

app = createApp()




# development only
if __name__ == '__main__':
    app.run(debug=not app.config["PRODUCTION"], host='0.0.0.0', port=8000)

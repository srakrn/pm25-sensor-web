import sys

activate_this = '/var/www/html/aqi/env/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))
sys.path.insert(0, '/var/www/html/aqi')
from cpe_pm25 import app as application

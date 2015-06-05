activate_this = '/home/code/sites/graphics.dailybruin/define-your-dorm/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))
import sys
sys.path.insert(0, '/home/code/sites/graphics.dailybruin/define-your-dorm')
from dorm import app as application
application.secret_key = "d8896aae58a83df06aef5f25b52b4d4f497c49f1"

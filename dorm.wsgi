activate_this = '/home/code/sites/graphics.dailybruin/define-your-dorm/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))
import sys
sys.path.insert(0, '/home/code/sites/graphics.dailybruin/define-your-dorm')
from dorm import app as application

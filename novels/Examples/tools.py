import sys
sys.path.append('.')

from novels.tools.get_list import *
from novels.tools.rename import *
from novels.tools.translate import *

# Translate
path = ''
tf = Translate(path)
tf.translate_all()
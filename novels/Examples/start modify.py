import sys
sys.path.append('.')

from novels.tools.modify import *

# change the username='', password='' in novels.core.epub_ln.py with lightnovel.cn account
# Run codes like example.py


folder = '/Volumes/Storage/Mine/Novels'
#folder = '/Volumes/Storage/Downloads'

for root, dirs, files in sorted(os.walk(folder)):
    for file in files:
        if file.split('.')[-1] in ['epub']:
            try:
                path = os.path.join(root, file)
                print(path)
                m = Modify(path)
            except Exception as e:
                print('Error', path)

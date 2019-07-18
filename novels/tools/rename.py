import re
import os

class RenameFiles:

    def __init__(self, folder):
        self.folder = folder

    def walk(self):
        for root, dirs, files in os.walk(self.folder):
            for dir in dirs:
                path = root + '/' + dir
                print(path)
            for file in files:
                path = root + '/' + file
                print(path)

    def rename(self, pattern, replacement):
        # rename files
        for root, dirs, files in os.walk(self.folder):
            for file in files:
                path = root + '/' + file
                if re.search(pattern, file):
                    new_path = root + '/' + re.sub(pattern, replacement, file)
                    os.rename(path, new_path)
                    print(new_path)
            for dir in dirs:
                path = root + '/' + dir
                if re.search(pattern, dir):
                    new_path = root + '/' + re.sub(pattern, replacement, dir)
                    os.rename(path, new_path)
                    print(new_path)
        # rename root folder
        path = self.folder
        name = os.path.basename(path)
        root = os.path.dirname(path)
        if re.search(pattern, name):
            new_path = root + '/' + re.sub(pattern, replacement, name)
            os.rename(path, new_path)



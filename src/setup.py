from shutil import rmtree, copytree
from os import listdir, mkdir, path

def setup_project():
    if (path.exists('public')):
        rmtree('public')
    copytree('static','public')
    print(listdir())

from shutil import rmtree, copytree
from os import listdir, mkdir, path
from utils import generate_page

def setup_project():
    if (path.exists('public')):
        rmtree('public')
    copytree('static','public')
    generate_page('content/index.md', 'template.html','public/index.html')
    print(listdir())

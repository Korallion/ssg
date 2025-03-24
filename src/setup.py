from shutil import rmtree, copytree
from os import listdir, mkdir, path
from utils import generate_pages_recursive

def setup_project():
    if (path.exists('public')):
        rmtree('public')
    copytree('static','public')
    generate_pages_recursive('content', 'template.html', 'public')

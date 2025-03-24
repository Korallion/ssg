from shutil import rmtree, copytree
from os import listdir, mkdir, path
from utils import generate_pages_recursive

def setup_project(basepath):
    if (path.exists('docs')):
        rmtree('docs')
    copytree('static','docs')
    generate_pages_recursive('content', 'template.html', 'docs', basepath)

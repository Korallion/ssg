from setup import setup_project
from sys import argv

def main():
    basepath = argv[1] if len(argv) > 1 else '/'
    print(f"basepath: {basepath}")
    setup_project(basepath)

main()

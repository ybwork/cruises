import os
import sys
from modulefinder import ModuleFinder


def install_env():
    os.system('virtualenv venv')


installer = ModuleFinder()


def install_modules():
    installer.run_script('scraping.py')

    for module in installer.badmodules.keys():
        os.system('pip install {module}'.format(module=module))


def main():
    install_env()
    install_modules()


if __name__ == '__main__':
    main()
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
    try:
        install_env()
        install_modules()
    except (NameError, TypeError):
        print('Something went wrong, try again later.')


if __name__ == '__main__':
    main()
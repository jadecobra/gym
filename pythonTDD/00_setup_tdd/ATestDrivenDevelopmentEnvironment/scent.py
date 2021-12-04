from sniffer.api import *
from subprocess import run

@runnable
def execute_nose(*args):
    if run('python -m unittest -f', shell=True).returncode != 0:
        return False

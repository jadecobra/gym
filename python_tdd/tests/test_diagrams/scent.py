import sniffer.api
import subprocess

@sniffer.api.runnable
def run_tests(*args):
    return subprocess.run('python -m unittest -f', shell=True).returncode == 0
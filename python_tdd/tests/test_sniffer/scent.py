import sniffer.api
import subprocess

@sniffer.api.runnable
def run_tests(*args):
    if subprocess.run('python3 -m unittest -f', shell=True).returncode == 0:
        return True

import sniffer.api
import subprocess


@sniffer.api.runnable
def run_tests(*args):
    if subprocess.run("python -m unittest -f tests/*.*", shell=True).returncode == 0:
        return True

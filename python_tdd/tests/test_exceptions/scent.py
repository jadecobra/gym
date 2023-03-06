import sniffer.api
import subprocess

watch_paths = [
    '.',
    'tests/',
    'tests/templates/',
]

@sniffer.api.runnable
def run_tests(*args):
    if subprocess.run('python -m unittest -f', shell=True).returncode == 0:
        return True
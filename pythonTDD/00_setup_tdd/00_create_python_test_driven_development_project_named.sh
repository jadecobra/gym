# Create a Python Test Driven Development Environment on Mac OS X
#   default project name is testDrivenDevelopmentEnvironment
source ../../helper

get_project_name () {
    read -p "What is the name of the Test Driven Development Environment: " environmentName
    [[ -z $environmentName ]] && environmentName="ATestDrivenDevelopmentEnvironment" || echo
    echo "\tenvironmentName: $environmentName"
    pause
}

create_directory_structure() {
    header "Create directory structure: $environmentName/tests..."
    mkdir -p $environmentName/tests
    cd $environmentName
    display_directory
}

create_boiler_plate_code() {
    header "Create boiler plate code..."
    touch $environmentName.py
    touch tests/__init__.py
    display_directory
}

create_failing_test() {
    header 'Create a failing python test...'
    cat << DELIMITER > tests/test_$environmentName.py
from unittest import TestCase

class Test$environmentName(TestCase):

    def test_failure(self):
        self.assertTrue(False)
DELIMITER
    cat tests/test_$environmentName.py
    display_directory
    pause
}

setup_virtual_environment () {
    header "Setup virtual environment..."
    python3 -m venv .venv
    display_directory
    source .venv/bin/activate
    pip install -U pip
    pip install sniffer macFSevents
}

create_scent_file() {
    header "Create scent file..."
    cat << DELIMITER > scent.py
from sniffer.api import *
from subprocess import run

@runnable
def execute_nose(*args):
    if run('python -m unittest -f', shell=True).returncode == 0:
        return True

DELIMITER
    cat scent.py
    display_directory
}

run_tests() {
    header 'Run tests...'
    code tests/test_$environmentName.py # you can change "code"" to match your editor
    sniffer
}

clear
header 'Creating a Python Test Driven Development Environment on Mac OS X'
get_project_name
create_directory_structure
create_boiler_plate_code
create_failing_test
setup_virtual_environment
create_scent_file
code tests/test_$environmentName.py
run_tests
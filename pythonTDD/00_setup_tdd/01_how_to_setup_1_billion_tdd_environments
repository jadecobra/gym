setupPythonTestDrivenDevelopmentEnvironmentForProjectNamed () {
    projectName=$1                  # What is the name of this project
    mkdir -p $projectName/tests
    cd $projectName

    touch $projectName.py
    touch tests/__init__.py
cat << DELIMITER > tests/test_$projectName.py
from unittest import TestCase

class Test$projectName(TestCase):

    def test_failure(self):
        self.assertTrue(False)
DELIMITER

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -U pip
    pip install sniffer macFSevents
}

for projectName in {1..1}
do
    setupPythonTestDrivenDevelopmentEnvironmentForProjectNamed $projectName
done
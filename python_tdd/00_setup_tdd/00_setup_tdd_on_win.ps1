projectName=$args[0]
mkdir -p $projectName/tests
Set-Location $projectName

New-Item tests/__init__.py
$testSetup = @"
from unittest import TestCase

class Test$($projectName)(TestCase):

    def test_failure(self):
        self.assertTrue(False)
"@
$testSetup |  Out-File $("tests/test_$($projectName).py") -Encoding UTF8

python -m venv ".$projectName"
.$projectName/scripts/activate
pip install -U pip
pip install sniffer macFSevents
sniffer
project_name="jadecobra"
rm -rf $project_name

mkdir -p $project_name/src/$project_name
mkdir -p $project_name/tests

cd $project_name

cat << EOF > pyproject.toml
[project]
name = "$project_name"
version = "0.0.2"
authors = [
  { name="johnnyblase", email="johnnyblasin@gmail.com" },
]
description = "DRY"
readme = "README.md"
license = { file="LICENSE" }
requires-python = ">=3.9"
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]

[project.urls]
"Homepage" = "https://github.com/pypa/sampleproject"
"Bug Tracker" = "https://github.com/pypa/sampleproject/issues"
EOF

cat << EOF > README.md
# Example package
DRY
EOF

cat << EOF > LICENSE
Copyright (c) 2022 JadeCobra LLC

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF

touch tests/__init__.py
cat << EOF > tests/test_$project_name.py
import unittest
import src.$project_name

class Test$project_name(unittest.TestCase):

    def test_failure(self):
        self.assertFalse(True)
EOF

cat << EOF > tests/test_z_build.py
import os
import unittest


class TestBuild(unittest.TestCase):

    def test_z_build(self):
        os.system('python3 -m build')
        # os.system('python3 -m twine upload dist/*')
EOF

cat << EOF > scent.py
import sniffer.api
import subprocess
watch_paths = ['tests/', 'src/']

@sniffer.api.runnable
def run_tests(*args):
    if subprocess.run("python -m unittest -f tests/*.*", shell=True).returncode == 0:
        return True
EOF

cat << EOF > src/$project_name/__init__.py
from . import $project_name
EOF

cat << EOF > src/$project_name/"$project_name".py
def test_failure():
    assert True == False
EOF

python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -U pip sniffer macfsevents twine wheel build
python3 -m pip uninstall nose -y

# pwd
# ls

# how to install package
# python3 -m venv .venv
# python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps $project_name
project_name=$1
mkdir -p $project_name/src/$project_name
cd $project_name
mkdir tests
touch src/$project_name/__init__.py
touch src/$project_name/project_name.py
touch LICENSE

cat << EOF > README.md
# Example package

This is a simple example package.
You can use [Github-flavored Markdown](https://guides.github.com/features/mastering-markdown/) to write your content.
EOF

cat << EOF > pyproject.toml
[build-system]
requires = [
    "setuptools",
    "wheel",
]
build-backend = "setuptools.build_meta"
EOF

cat << EOF > setup.cfg
[metadata]
name = example-package-jakeitegsy
version = 0.0.1
author = jadecobra
author_email = jakeitegsy@yahoo.com
description = A small example package
long_description = file: README.md
long_description_content_type = text/markdown
url = https://github.com/pypa/sampleproject
project_urls =
    Bug Tracker = https://github.com/pypa/sampleproject/issues
classifiers =
    Programming Language :: Python :: 3
    License :: OSI Approved :: MIT License
    Operating System :: OS Independent

[options]
package_dir =
    = src
packages = find:
python_requies = >=3.6

[options.packages.find]
where = src
EOF

python3 -m pip install --upgrade build
python3 -m build
python3 -m install --upgrade twine
python3 -m twine upload --repository testpypi dist/*

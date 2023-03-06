import os

def install_package(package):
    return os.system(f"pip install {package}")

def install_specific_version(package=None, version=None):
    return os.system(f"pip install {package}=={version}")

def install_minimum_version(package=None, version=None):
    return os.system(f"pip install {package}>={version}")

def upgrade_package(package):
    return os.system(f"pip install --upgrade {package}")

def install_package_for_current_user(package):
    return os.system(f"pip install --user {package}")

pip install git+https://github/jadecobra/repo.git
pip install git+//github.com/jadecobra/mock_boto3.git
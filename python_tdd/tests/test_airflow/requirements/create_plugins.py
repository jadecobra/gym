import os
import sys
import shutil

def create_offline_requirements(constraints):
    offline_requirements = f"{constraints[:-4]}_offline.txt"
    with (
        open(constraints) as source,
        open(offline_requirements, 'w') as target,
    ):
        target.write('--find-links /usr/local/airflow/plugins\n')
        target.write('--no-index\n')
        target.write(source.read())
    return offline_requirements

def clean_up(filename):
    try:
        os.remove(filename)
    except FileNotFoundError:
        pass
    except Exception:
        shutil.rmtree(filename, ignore_errors=True)

def create_zip_file(directory=None, constraints=None):
    zip_file = f'{constraints[:-4]}.zip'
    clean_up(zip_file)
    os.chdir(directory)
    os.system(f'7z a {zip_file} . -mx1 -mmt')
    shutil.move(zip_file, f'../plugins.zip')
    os.chdir('..')
    return zip_file

def get_dependencies(directory=None, constraints=None):
    os.makedirs(directory, exist_ok=True)
    os.system('python3 -m pip install -U pip')
    os.system(
        f'python3 -m pip download -r {constraints} -d {directory}'
        # f'pip download --python-version 310 --only-binary=:all: -r {constraints} -d {directory}'
        # f'pip download --python-version 310 --only-binary=:all: --implementation cp --implementation py -r {constraints} -d {directory}'
        # f'pip download -r {constraints} -d {directory} --platform manylinux2014_x86_64 --platform linux_x86_64 --platform linux_i386 --platform any --abi --implementation py --implementation cp --only-binary=:all:'
        # f'pip download -r {constraints} -d {directory} --abi --implementation py --implementation cp --only-binary=:all:'
        # f'pip download -r {constraints} -d {directory}--abi --implementation cp --only-binary=:all:'
        # f'pip download -r {constraints} -d {directory}--abi --implementation cp --only-binary=:all:'
        # f'pip download -r {constraints} -d {directory} --implementation cp --implementation py --only-binary=:all:'
    )

def upload_to_s3(requirements=None, zip_file=None):
    s3_path = 's3://'
    for command in (
        f'{requirements_file} {s3_path}/requirements/{requirements_file}',
        f'{zip_file} {s3_path}/plugins/{zip_file}'
    ):
        os.system(f'aws s3 cp {command}')

if __name__ == '__main__':
    try:
        constraints = sys.argv[1].split('.\\')[1]
    except IndexError:
        constraints = sys.argv[1]

    os.system('clear')
    directory = 'plugins'
    clean_up(directory)
    get_dependencies(
        directory=directory,
        constraints=constraints,
    )
    requirements_file = create_offline_requirements(constraints)
    zip_file = create_zip_file(
        directory=directory,
        constraints=constraints,
    )
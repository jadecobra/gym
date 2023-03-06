import os

def create_scent(filename=None, extensions=None, prefix='run'):
    with open(f'{filename}.py', 'w') as file:
        file.write('import sniffer.api\n\n')
        for extension in extensions:
            runner_name = f'{prefix}_{extension}'
            file.writelines(f"""
@sniffer.api.runnable
def {runner_name}(mock, *args):
    mock(*args)

@sniffer.api.select_runnable("{runner_name}")
@sniffer.api.file_validator
def {extension}(filename):
    return filename.endswith("{extension}")
"""
    )

def delete_scent(filename):
    os.remove(f'{filename}.py')
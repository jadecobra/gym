"""
Loads a `scent.py` configuration file for sniffer and extracts the values there
"""
from __future__ import print_function
import os
import sys
import termstyle


class ScentModule(object):


    def __init__(self, module=None, filename=None):
        self.module = module
        self.filename = filename
        self.runner_name = None
        self.runners, self.file_validators = self.get_runners_and_validators()
        self.runners = tuple(self.runners)
        self.file_validators = tuple(self.file_validators)

    def get_scent_api_type(self, obj):
        return getattr(obj, 'scent_api_type', None)

    def add_agent(self, module_name=None, runners=None, file_validators=None):
        if self.get_scent_api_type(module_name) == 'runnable':
            runners.append(module_name)
        if self.get_scent_api_type(module_name) == 'file_validator':
            file_validators.append(module_name)
        return runners, file_validators

    def get_module_name(self, name=None):
        return getattr(self.module, name)

    def get_runners_and_validators(self):
        runners = []
        file_validators = []
        for name in dir(self.module):
            self.add_agent(
                self.get_module_name(name),
                runners=runners,
                file_validators=file_validators
            )
        return runners, file_validators

    def reload(self):
        try:
            return get_scent(self.filename)
        except Exception as error:
            print(error)
            print("Still using previously valid Scent.")
            return self

    def run(self, args):
        try:
            for runner in self.get_runners():
                if not runner(*args):
                    return False
            return True
        except Exception:
            import traceback
            traceback.print_exc()
            print()
            return False

    def set_runner(self, runner_name):
        self.runner_name = runner_name

    def get_runners(self):
        if self.runner_name:
            return tuple(
                filter(
                    lambda f: f.__name__ == self.runner_name,
                    self.runners
                )
            )
        return tuple(self.runners)

    @property
    def fg_pass(self):
        return getattr(self.module, 'pass_fg_color', termstyle.black)

    @property
    def bg_pass(self):
        return getattr(self.module, 'pass_bg_color', termstyle.bg_green)

    @property
    def fg_fail(self):
        return getattr(self.module, 'fail_fg_color', termstyle.white)

    @property
    def bg_fail(self):
        return getattr(self.module, 'fail_bg_color', termstyle.bg_red)

    @property
    def watch_paths(self):
        return getattr(self.module, 'watch_paths', ('.',))



def delete_module_from_sys(module):
    if module in sys.modules:
        del sys.modules[module]

def add_module_to_sys(module):
    if module not in set(sys.modules.keys()):
        sys.path.insert(0, module)

def get_module(name):
    global_variables = globals().copy()
    return __import__(name, global_variables, global_variables)

def get_module_name(filename):
    return '.'.join(os.path.basename(filename).split('.')[:-1])

def get_scent(filename):
    "Runs the given scent.py file."
    module_name = get_module_name(filename)
    delete_module_from_sys(module_name)
    add_module_to_sys(os.path.dirname(filename))
    return ScentModule(
        module=get_module(module_name),
        filename=filename
    )

def exec_from_dir(dirname=None, scent="scent.py"):
    """Runs the scent.py file from the given directory (cwd if None given).

    Returns module if loaded a scent, None otherwise.
    """
    if dirname is None:
        dirname = os.getcwd()
    files = os.listdir(dirname)

    if scent not in files:
        return None

    return get_scent(os.path.join(dirname, scent))

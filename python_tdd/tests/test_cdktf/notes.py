from lib2to3.pytree import convert


import os

def cdk_tf(command):
    return os.system(f'cdktf {command}')

def convert_hcl_to_cdk(filename):
    return cdk_tf(f'convert {filename}')

def deploy(stack):
    return cdk_tf(f'deploy {stack}')

def diff(stack):
    return cdk_tf(f'diff {stack}')

def get(options):
    return cdk_tf(f'get {options}')

def create_new_project():
    return cdk_tf(f'init')

def list_stacks(options):
    return cdk_tf(f'list {options}')

def get_terraform_cloud_api_key(options):
    return cdk_tf('login')

def synth(stack):
    return cdk_tf(f'synth {stack}')

def watch(stack):
    return cdk_tf(f'watch {stack}')

def create_completion_script():
    return cdk_tf('completion')
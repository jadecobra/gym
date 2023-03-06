import sniffer.api

@sniffer.api.runnable
def execute_ext0(mock, *args):
    mock('ext0')

@sniffer.api.runnable
def execute_ext1(mock, *args):
    mock('ext1')

@sniffer.api.runnable
def execute_ext2(mock, *args):
    mock('ext2')

@sniffer.api.runnable
def execute_ext3(mock, *args):
    mock('ext3')


@sniffer.api.select_runnable('execute_ext0')
@sniffer.api.file_validator
def ext0_files(filename):
    return filename.endswith('.ext0')

@sniffer.api.select_runnable('execute_ext1')
@sniffer.api.file_validator
def ext1_files(filename):
    return filename.endswith('.ext1')

@sniffer.api.select_runnable('execute_ext2')
@sniffer.api.file_validator
def ext2_files(filename):
    return filename.endswith('.ext2')

@sniffer.api.select_runnable('execute_ext3')
@sniffer.api.file_validator
def ext3_files(filename):
    return filename.endswith('.ext3')
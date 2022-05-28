import cProfile
import pstats
import sys


def run(command=None, filename=None, sort=-1):
    return cProfile.run(command, filename=filename, sort=sort)


def run_ctx(command=None, globals=None, locals=None, filename=None, sort=-1):
    return cProfile.runctx(command, globals, locals, filename=filename, sort=-1)


class Profile:
    def __init__(self, timer=None, time_unit=0.0, sub_calls=True, built_ins=True):
        self.profiler = cProfile.Profile(
            timer=timer,
            timeunit=time_unit,
            subcalls=sub_calls,
            builtins=built_ins,
        )

    def start_collecting_profiling_data(self):
        return self.profiler.enable()

    def stop_collecting_profiling_data(self):
        return self.profiler.disable()

    def stop_collecting_profiling_data_records_results_as_current_profile(self):
        return self.profiler.create_stats()

    def create_stats_object_based_on_current_profile(self, sort=-1):
        return self.profiler.print_stats(sort)

    def write_stats_to_file(self, filename):
        return self.profiler.dump_stats(filename)

    def profile(self, command):
        return self.profiler.run(command)

    def profile_with_globals_and_locals(self, command=None, globals=None, locals=None):
        return self.profiler.runctx(command, globals, locals)

    def profile_function(self, function, /, *args, **kwargs):
        return self.profiler.runcall(function, args, kwargs)


class Analyzer(object):
    def __init__(self, *filenames, stream=sys.stdout):
        self.analyst = pstats.Stats(*filenames, stream=stream)

    def remove_leading_path_from_filenames(self):
        return self.analyst.strip_dirs()

    def add_additional_profiling(self, *filenames):
        return self.analyst.add(filenames)

    def write_stats_to_file(self, filename):
        return self.analyst.dump_stats(filename)

    def sort_statistics(self, *keys):
        return self.analyst.sort_stats(keys)

    def reverse_order(self):
        return self.analyst.reverse_order()

    def display_statistics(self, *restrictions):
        return self.analyst.print_stats(restrictions)

    def print_callers(self, *restrictions):
        return self.analyst.print_callers(restrictions)

    def print_callees(self, *restrictions):
        return self.analyst.print_callees(restrictions)

    def get_stats_profile(self):
        return self.analyst.get_stats_profile()
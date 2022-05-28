import unittest
import cProfile
import pstats

# import re

# cProfile.run('re.compile("foo|bar")')

# '''python -m cProfile [-o output_file] [-s sort_order] (-m module | myscript.py)'''
class TestProfiling(unittest.TestCase):
    maxDiff = None

    def test_failure(self):
        self.assertFalse(False)

    def test_profiler_context_manager(self):
        with cProfile.Profile() as profiler:
            print("jake")
            analyst = pstats.Stats(profiler)
            # self.assertEqual(
            #     dir(analyst.print_stats()),
            #     [
            #         "__class__",
            #         "__delattr__",
            #         "__dict__",
            #         "__dir__",
            #         "__doc__",
            #         "__eq__",
            #         "__format__",
            #         "__ge__",
            #         "__getattribute__",
            #         "__gt__",
            #         "__hash__",
            #         "__init__",
            #         "__init_subclass__",
            #         "__le__",
            #         "__lt__",
            #         "__module__",
            #         "__ne__",
            #         "__new__",
            #         "__reduce__",
            #         "__reduce_ex__",
            #         "__repr__",
            #         "__setattr__",
            #         "__sizeof__",
            #         "__str__",
            #         "__subclasshook__",
            #         "__weakref__",
            #         "add",
            #         "all_callees",
            #         "calc_callees",
            #         "dump_stats",
            #         "eval_print_amount",
            #         "fcn_list",
            #         "files",
            #         "get_print_list",
            #         "get_sort_arg_defs",
            #         "get_stats_profile",
            #         "get_top_level_stats",
            #         "init",
            #         "load_stats",
            #         "max_name_len",
            #         "prim_calls",
            #         "print_call_heading",
            #         "print_call_line",
            #         "print_callees",
            #         "print_callers",
            #         "print_line",
            #         "print_stats",
            #         "print_title",
            #         "reverse_order",
            #         "sort_arg_dict",
            #         "sort_arg_dict_default",
            #         "sort_stats",
            #         "stats",
            #         "stream",
            #         "strip_dirs",
            #         "top_level",
            #         "total_calls",
            #         "total_tt",
            #     ],
            # )
            # self.assertIsNone(profiler.print_stats())
            for key, value in analyst.get_stats_profile().func_profiles.items():
                print(key, ":", value)
            # print(analyst.get_stats_profile().func_profiles)
            self.assertEqual(analyst.get_stats_profile().func_profiles, [])


# cProfile.run(command, filename=None, sort=-1)
# cProfile.runctx(command, globals, locals, filename=None, sort=-1)
# cProfile.Profile()

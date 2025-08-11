#!/usr/bin/python


from importlib.metadata import version
import argparse

description = """

"""

epilog = """
"""


# 80-23=57 spaces wide

version_help = f'\
timelog ver. {version("xyzutils")}'

add_help = """
ddad
"""

delete_help = """
dsds
"""

category_help = """
fsfsf
"""

results_help = """
fsfsf
"""

show_help = """
stst
"""

start_help = """
stst
"""

stop_help = """
tptp
"""


def argument_parser():
    parser = argparse.ArgumentParser(
        prog='tlog',
        description=description,
        epilog=epilog,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        '--version', action='version',
        version=version_help,
    )
    parser.add_argument(
        '-a', '--add', nargs='*',
        help=add_help,
    )
    parser.add_argument(
        '-d', '--delete', nargs='*',
        help=delete_help,
    )
    parser.add_argument(
        '-c', '--category',
        help=category_help,
    )
    parser.add_argument(
        '-r', '--results', action='store_true',
        help=results_help,
    )
    parser.add_argument(
        '-s', '--show',
        help=show_help,
    )
    parser.add_argument(
        '--start',
        help=start_help,
    )
    parser.add_argument(
        '--stop',
        help=stop_help,
    )
    """
    parser.add_argument(
        'input', nargs='+', default=[],
        help=input_help,
    )
    op = parser.add_argument_group(
        'db operations',
    )
    op.add_argument(
        '-m', '--merge', action='store_true',
        help=merge_help,
    )
    op.add_argument(
        '-o', '--output', default=False,
        help=output_help,
    )
    """
    
  
    return parser.parse_args()

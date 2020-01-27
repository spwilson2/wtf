from __future__ import print_function

import argparse
import os
import re

#############################
# Constants
# Constants
#############################

#############################
# Script utilities

# ABC for subcommands
class Subcommand(object):
    name = None

    def init_parser(self, subparser):
        raise NotImplementedError

    def process_args(self, parser, args):
        raise NotImplementedError

    def run(self, multi):
        raise NotImplementedError


def parse_args(argv):
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')
    subparsers.required = True

    subcommands = Subcommand.__subclasses__()

    # Instantiate subcommand objects from their class,
    # assign them their name used by the parser
    # (sc -> subcommand)
    commands = {}
    for sc in subcommands:
        assert sc.name is not None, ('Subclass %s name not set in class'
            'definition' % str(sc))
        assert sc.name not in commands, 'Multiple commands with the same name'
        commands[sc.name] = sc()

    # Initialize all subparsers
    for name, sc in commands.items():
        subparser = subparsers.add_parser(name, help=sc.__doc__)
        sc.init_parser(subparser)

    # Parse arguments and get subcommand
    options = parser.parse_args(argv)
    sc = commands[options.command]
    sc.post_process_args(parser, options)
    return sc

# Script utilities
#############################

class RunSubcommand(Subcommand):
    name = 'run'
    def __init__(self):
        self._sentinel = object()

    def init_parser(self, subparser):
        # Default = os.getcwd()
        #subparser.add_argument('path', default=None, required=False)
        pass

    def post_process_args(self, parser, args):
        # Set defaults if none-provided

        if args.rtos_path is self._sentinel:
            args.rtos_path = os.path.abspath(os.path.join(args.bsp_path, ".."))

        if args.flash_script is self._sentinel:
            args.flash_script = GET_DEFAULT_FLASH_SCRIPT_PATH(args.bsp_path)

        # Verify that the given bootloader_dir is correct
        search_paths = [args.rtos_path, args.bsp_path]
        binary_path = FindFilePath(search_paths, args.bootloader_dir)
        check_is_file(binary_path)

        self.args = args

    def run(self, multi):
        cmds = get_rcar_uboot_flash_commands(
                self.args.flash_script, self.args.bootloader_dir)

        for cmd in cmds:
            multi.run_flash_command(cmd)
        return 0


################################################
# Boilerplate for a standalone importable script

def main(argv):
    command = parse_args(argv)
    command.run(multi)
    return 0


def entrypoint():
    '''
    Script entrypoint.
    '''
    sys.exit(main(sys.argv[1:]))


if __name__ == '__main__':
    entrypoint()

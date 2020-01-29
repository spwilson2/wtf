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
class Subcommand(object):
    '''
    ABC for subcommands
    '''
    name = None

    # A sentinal object used by subcommands to check if no argument was
    # provided.
    _sentinel = object()

    def init_parser(self, subparser):
        raise NotImplementedError

    def post_process_args(self, parser, args):
        # Set defaults if none-provided
        self.args = args

    def run(self, multi):
        raise NotImplementedError

    @classmethod
    def parse_args(cls, argv):
        parser = argparse.ArgumentParser()
        cls.init_common_parser(parser)

        subparsers = parser.add_subparsers(dest='command')
        subparsers.required = True

        subcommands = cls.__subclasses__()

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

    @classmethod
    def init_common_parser(cls, parser):
        '''
        Initialize common arguments for all subcommands.
        '''
        pass


# Script utilities
#############################

def setup():
    # Setup Logging
    pass

# TODO Logging framework 
# - Save output of python tests? 
# - Save output of spawned processes
#
# - Enable tests to access output of spawned processes

# TODO Sandbox tests
# - Failed tests should not take down the test runner
#  -> Use clone (not multiprocessing)


class RunSubcommand(Subcommand):
    name = 'run'
    def __init__(self):
        pass

    def init_parser(self, subparser):
        # Default = os.getcwd()
        # subparser.add_argument('path', default=self._sentinel, required=False)
        pass

    def run(self):
        # TODO :
        # Crawl the test tree, enumerating test object
        return 0


################################################
# Boilerplate for a standalone importable script

def main(argv):
    command = Subcommand.parse_args(argv)
    command.run()
    return 0


def entrypoint():
    '''
    Script entrypoint.
    '''
    sys.exit(main(sys.argv[1:]))


if __name__ == '__main__':
    entrypoint()

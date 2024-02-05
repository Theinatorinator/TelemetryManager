#    Copyright 2024 Logan Mamanakis

#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at

#        http://www.apache.org/licenses/LICENSE-2.0

#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

from .stores.RepoManager import RepoManager
import argparse
import logging
Logger = logging.getLogger(__name__)


class TelemetryManager:

    def __init__(self):
        self.repo_manager = RepoManager()

        self.parse_args()

        logging.basicConfig(
            level=self.args.logLevel, format='%(asctime)s - %(levelname)s: %(message)s')

        Logger.info("Running with arguments: %s", self.args)

        self.args.func(self.args)

    def parse_args(self):
        # Argument parsing
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(required=True)

        git_dir_parser_parent = argparse.ArgumentParser()
        git_dir_parser_parent.add_argument(
            '--dir',
            help="The directory git repo used to store all the logs",
            action='store',
            dest='repo_path',
            required=True)

        parser.add_argument(
            '--debug',
            help="Print lots of debugging statements",
            action="store_const",
            dest="logLevel",
            const=logging.DEBUG,
            default=logging.WARNING,
        )

        parser.add_argument(
            '-v',
            '--verbose',
            help="Be verbose",
            action="store_const",
            dest="logLevel",
            const=logging.INFO,
        )

        parser_git = subparsers.add_parser('git')

        parser_git_subparsers = parser_git.add_subparsers(required=True)

        parser_git_lock = parser_git_subparsers.add_parser(
            'lock', parents=[git_dir_parser_parent], add_help=False)

        parser_git_lock.set_defaults(func=self.repo_manager.lock)

        parser_git_init = parser_git_subparsers.add_parser(
            'init', parents=[git_dir_parser_parent], add_help=False)

        parser_git_init.set_defaults(func=self.repo_manager.init)

        parser_git_clone = parser_git_subparsers.add_parser(
            'clone', parents=[git_dir_parser_parent], add_help=False)

        parser_git_clone.add_argument(
            '-u',
            '--url',
            help="The URL of remote git repo to clone",
            action='store',
            dest='repo_url',
            required=True
        )

        parser_git_clone.set_defaults(func=self.repo_manager.clone)

        self.args = parser.parse_args()

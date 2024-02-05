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

from .stores.GitRepoManager import GitRepoManager
import argparse
import logging
Logger = logging.getLogger(__name__)


class TelemetryManager:

    def __init__(self):
        self.repo_manager = GitRepoManager()

        self._init_arg_parser()
        self._parse_args()

        self.interactive(None)

        logging.basicConfig(
            level=self.args.logLevel, format='%(asctime)s - %(levelname)s: %(message)s')

        Logger.info("Running with arguments: %s", self.args)

        self.args.func(self.args)

    def _init_arg_parser(self):
        # Argument parsing
        self._parser = argparse.ArgumentParser()
        self._subparsers = self._parser.add_subparsers(required=True)

        self._git_dir_parser_parent = argparse.ArgumentParser()
        self._git_dir_parser_parent.add_argument(
            '--dir',
            help="The directory git repo used to store all the logs",
            action='store',
            dest='repo_path',
            required=True)

        self._parser.add_argument(
            '--debug',
            help="Print lots of debugging statements",
            action="store_const",
            dest="logLevel",
            const=logging.DEBUG,
            default=logging.WARNING,
        )

        self._parser.add_argument(
            '-v',
            '--verbose',
            help="Be verbose",
            action="store_const",
            dest="logLevel",
            const=logging.INFO,
        )

        self._parser_git = self._subparsers.add_parser('git')

        self._parser_git_subparsers = self._parser_git.add_subparsers(
            required=True)

        self._parser_git_lock = self._parser_git_subparsers.add_parser(
            'lock', parents=[self._git_dir_parser_parent], add_help=False)

        self._parser_git_lock.set_defaults(func=self.repo_manager.lock)

        self._parser_git_init = self._parser_git_subparsers.add_parser(
            'init', parents=[self._git_dir_parser_parent], add_help=False)

        self._parser_git_init.set_defaults(func=self.repo_manager.init)

        self._parser_git_clone = self._parser_git_subparsers.add_parser(
            'clone', parents=[self._git_dir_parser_parent], add_help=False)

        self._parser_git_clone.add_argument(
            '-u',
            '--url',
            help="The URL of remote git repo to clone",
            action='store',
            dest='repo_url',
            required=True
        )

        self._parser_git_clone.set_defaults(func=self.repo_manager.clone)

        self._parser_cmd = self._subparsers.add_parser('cmd')

    def _parse_args(self) -> None:
        self.args = self._parser.parse_args()

    def interactive(self, args) -> None:
        while True:
            locked = "X" if self.repo_manager.ready() else ""
            uin = input("TelemetryManager " + "[" + locked +"]"+">")
            try:
                self.args = self._parser.parse_args(uin.split())
            except:
                print("Error, Invalid Command!")
                continue
            print("ok")
            self.args.func(self.args)

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

from argparse import Namespace
import logging
import os
import re
from tabnanny import check
from time import sleep
from tokenize import String
from git import InvalidGitRepositoryError, Repo
Logger = logging.getLogger(__name__)


class RepoManager:

    def __init__(self):
        self._repo = None

    def checkAndLockRepo(self):
        try:
            self._repo = Repo(self.args.repo_path)
            Logger.info("Found and locked git repo at directory %s",
                        self.args.repo_path)
            return True
        except InvalidGitRepositoryError:
            Logger.info("No git repo found at directory!")

    def make_repo(self):
        Logger.info(
            "Creating repo in location %s", self.args.repo_path)
        self._repo = Repo.init(self.args.repo_path)

    def clone_repo(self):
        Logger.info("Cloning repo from %s to directory %s",
                    self.args.repo_url, self.args.repo_path)
        Repo.clone_from(url=self.args.repo_url,
                        to_path=self.args.repo_path)

    def no_repo(self):
        Logger.critical(
            """Git repo not found at path! Ensure you provide a path to an
                appropriate git repo. You may also use the init or clone commands to set up a repo.""")
        raise RuntimeError("Cannot continue without a repo!")

    def check_path(self):
        if os.path.isdir(self.args.repo_path) != True:
            Logger.critical("Invalid path %s", self.args.repo_path)
            raise RuntimeError("Invalid path")

    def _get_repo(self):
        return self._repo

    repo = property(fget=_get_repo)

    def lock(self, args: Namespace, repo_dir=None):

        if repo_dir is not None:
            self.args = Namespace(kwargs={'repo_dir': repo_dir})
        else:
            self.args = args

        self.check_path()
        if self.checkAndLockRepo():
            return True
        if self._repo == None:
            self.no_repo()

    def init(self, args: Namespace):
        self.args = args
        self.check_path()
        if self.checkAndLockRepo():
            return True
        self.make_repo()
        if self._repo == None:
            self.no_repo()

    def clone(self, args: Namespace):
        self.args = args
        self.check_path()
        if self.checkAndLockRepo():
            return True
        self.clone_repo()
        self.checkAndLockRepo()
        if self._repo == None:
            self.no_repo()

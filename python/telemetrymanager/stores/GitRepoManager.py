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
from tabnanny import check
from time import sleep
from tokenize import String
from xmlrpc.client import Boolean
from git import InvalidGitRepositoryError, Repo

from .LogStore import LogStore

Logger = logging.getLogger(__name__)


class GitRepoManager(LogStore):

    def __init__(self) -> None:
        self._repo = None

    def _checkAndLockRepo(self) -> bool:
        try:
            self._repo = Repo(self.args.repo_path)
            Logger.info("Found and locked git repo at directory %s",
                        self.args.repo_path)
            return True
        except InvalidGitRepositoryError:
            Logger.info("No git repo found at directory!")
            return False

    def _make_repo(self) -> bool:
        Logger.info(
            "Creating repo in location %s", self.args.repo_path)
        try:
            self._repo = Repo.init(self.args.repo_path)
        except:
            return False
        return True

    def _clone_repo(self) -> bool:
        Logger.info("Cloning repo from %s to directory %s",
                    self.args.repo_url, self.args.repo_path)
        try:
            Repo.clone_from(url=self.args.repo_url,
                            to_path=self.args.repo_path)
        except:
            return False
        return True

    def _no_repo(self) -> None:
        Logger.critical(
            """Git repo not found at path! Ensure you provide a path to an
                appropriate git repo. You may also use the init or clone commands to set up a repo.""")
        raise RuntimeError("Cannot continue without a repo!")

    def _check_path(self) -> bool:
        if os.path.isdir(self.args.repo_path) != True:
            Logger.critical("Invalid path %s", self.args.repo_path)
            return False
        return True

    def _get_repo(self) -> Repo | None:
        return self._repo

    def _check_meta(self) -> bool:
        return False

    repo = property(fget=_get_repo)

    def lock(self, args: Namespace, repo_dir=None) -> bool:

        if repo_dir is not None:
            self.args = Namespace(kwargs={'repo_dir': repo_dir})
        else:
            self.args = args

        self._check_path()

        if self._checkAndLockRepo():
            return True
        if self._repo == None:
            return False

        return False

    def init(self, args: Namespace) -> bool:
        self.args = args
        self._check_path()
        if self._checkAndLockRepo():
            return True
        self._make_repo()
        if self._repo == None:
            self._no_repo()
        return True

    def clone(self, args: Namespace) -> bool:
        self.args = args
        self._check_path()
        if self._checkAndLockRepo():
            return True
        self._clone_repo()
        self._checkAndLockRepo()
        if self._repo == None:
            self._no_repo()
        return True

    def ready(self) -> bool:
        return self._repo is not None

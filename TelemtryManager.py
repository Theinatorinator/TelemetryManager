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

import argparse
import logging
import os
from git import Repo
Logger = logging.getLogger(__name__)

_repo = None

def main():
    # Argument parsing
    parser = argparse.ArgumentParser()
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
    parser.add_argument(
        "-d",
        "--directory",
        help="The directory git repo used to store all the logs",
        action="store",
        dest="repoPath")

    parser.add_argument(
        "-f",
        "--force",
        help="Force operations to happen, potentially overwriting files.",
        dest="forceEnabled",
        action="store_true")

    args = parser.parse_args()
    logging.basicConfig(
        level=logging.DEBUG, format='%(asctime)s - %(levelname)s: %(message)s')

    # Buisnes logic
    check_and_set_repo(args.repoPath, args.forceEnabled)


def check_and_set_repo(repo_path, do_init):
    if os.path.isdir != True:
        Logger.critical("Invalid path provided, check your options!")
        raise RuntimeError("Invalid path")

    _repo = Repo(repo_path)

    if _repo == None:
        if do_init == False:
            Logger.critical(
                """Git repo not found at path! Ensure you provide a path to an
                    appropriate git repo or use the f flag to force and intialize a new repo at the path.""")
            raise RuntimeError("No git repo found")
        else:
            Logger.info(
                "No git repo exsists, and we were authorized to create one. Creating!")
            _repo = Repo.init(repo_path)
    else:
        Logger.info("Repo was found at location!")


main()

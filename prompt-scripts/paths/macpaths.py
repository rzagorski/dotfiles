# -*- coding: utf-8 -*-
"""
Module to get straight and correct PATH variable
"""

import os

from paths.paths import Paths

class MacPaths(Paths):

    """
    macOS paths configuration
    """

    def __init__(self):
        self._paths = []
        self._python_versions_to_check = [
            '2.7',
            '3.4',
            '3.5'
        ]

    def add_paths(self, paths_list):
        """
        Add paths to current PATH

        :param list paths_list: Current paths
        """

        self._paths = paths_list

        self._move_brew_path_to_first_place()
        self._add_python_userbase_to_path()

    @property
    def paths(self):
        """
        Return modified paths list

        :rtype: list
        """

        return self._paths

    def _move_brew_path_to_first_place(self):
        """
        Move /usr/local/bin to first place on the list
        """

        brew_bin_path = '/usr/local/bin'
        self._remove_path_from_current_paths(brew_bin_path)
        self._paths.insert(0, brew_bin_path)

    def _add_python_userbase_to_path(self):
        """
        Add python modules binaries paths to PATH
        """

        for single_python_version in self._python_versions_to_check:
            print(single_python_version)
            python_binary_path = os.path.join('/usr/local/bin/', 'python{}'.format(single_python_version))

            if not os.path.exists(python_binary_path):
                continue

            python_bins_path = os.path.join(
                os.getenv('HOME'),
                'Library/Python/',
                single_python_version,
                'bin'
            )

            self._remove_path_from_current_paths(python_bins_path)
            self._paths.insert(
                0,
                python_bins_path
            )

    def _remove_path_from_current_paths(self, path_to_remove):
        """
        Remove path from paths

        :param str path_to_remove: Path to remove from current paths list.
        """

        try:
            self._paths.remove(path_to_remove)
        except ValueError:
            pass

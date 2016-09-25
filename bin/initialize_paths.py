# -*- coding: utf-8 -*-
"""
Module to get straight and correct PATH variable
"""

import os
import site
import sys


def main():
    """
    Create paths
    """

    current_paths = os.environ['PATH'].split(':')
    current_paths = move_brew_path_to_first_place(current_paths)
    current_paths = add_python_userbase_to_path(current_paths)
    current_paths = add_dotfiles_bin_path(current_paths)
    current_paths = add_local_node_modules_to_path(current_paths)

    print(
        ':'.join(current_paths)
    )


def move_brew_path_to_first_place(current_paths):
    """
    Move /usr/local/bin to first place on the list

    :param list current_paths: Current paths.

    :rtype: list
    """

    current_paths = remove_path_from_current_paths('/usr/local/bin', current_paths)
    current_paths.insert(0, '/usr/local/bin')
    return current_paths


def add_python_userbase_to_path(current_paths):
    """
    Add python paths to PATH

    :param list current_paths: Current paths.

    :rtype: list
    """

    python_3_path_to_bin = os.path.join(site.USER_BASE, 'bin')
    python_2_path_to_bin = python_3_path_to_bin.replace(
        '{major}.{minor}'.format(
            major=sys.version_info.major,
            minor=sys.version_info.minor
        ),
        '2.7'
    )

    current_paths = remove_path_from_current_paths(python_2_path_to_bin, current_paths)
    current_paths.insert(
        0,
        python_2_path_to_bin
    )

    current_paths = remove_path_from_current_paths(python_3_path_to_bin, current_paths)
    current_paths.insert(
        0,
        python_3_path_to_bin
    )

    return current_paths


def add_rbenv_path(current_paths):
    """
    Check if rbenv is available and add bin to PATH

    :param list current_paths: Current paths.

    :rtype: list
    """

    user_home = os.path.expanduser("~")
    rbenv_path = os.path.join(user_home, '.rbenv/bin')

    if os.path.exists(rbenv_path):
        current_paths = remove_path_from_current_paths(rbenv_path, current_paths)
        current_paths.append(rbenv_path)

    return current_paths


def add_local_node_modules_to_path(current_paths):
    """
    Add python paths to

    :param list current_paths: Current paths.

    :rtype: list
    """

    for single_path in current_paths:
        if 'node_modules' not in single_path:
            continue

        path_without_node_modules = single_path.replace('/node_modules/.bin', '')
        if path_without_node_modules not in os.getcwd():
            current_paths = remove_path_from_current_paths(single_path, current_paths)
    local_node_modules_path = os.path.join(os.getcwd(), 'node_modules/.bin')

    if os.path.exists(local_node_modules_path) and local_node_modules_path not in current_paths:
        current_paths.insert(0, local_node_modules_path)

    return current_paths


def add_dotfiles_bin_path(current_paths):
    """
    Add dotfiles bin directory

    :param list current_paths: Current paths.

    :rtype: list
    """

    user_home = os.path.expanduser("~")
    dotfiles_bin_path = os.path.join(user_home, '.dotfiles/bin')
    if dotfiles_bin_path not in current_paths:
        current_paths.append(
            dotfiles_bin_path
        )

    return current_paths


def remove_path_from_current_paths(path_to_remove, current_paths):
    """
    Remove path from paths

    :param str  path_to_remove: Path to remove from current paths list.
    :param list current_paths : Current paths.

    :rtype: list
    """

    try:
        current_paths.remove(path_to_remove)
    except ValueError:
        pass

    return current_paths

if __name__ == '__main__':
    main()

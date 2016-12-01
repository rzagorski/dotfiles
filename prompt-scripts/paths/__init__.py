# -*- coding: utf-8 -*-
"""
Module for paths
"""

from paths.generalpaths import GeneralPaths
from paths.macpaths import MacPaths


def create_general_paths():
    os_paths = MacPaths()
    return GeneralPaths([os_paths])

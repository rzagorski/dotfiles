# -*- coding: utf-8 -*-
"""
Module to get straight and correct PATH variable
"""
import click

from paths import create_general_paths


@click.group()
def cli():
    """
    Command group
    """
    pass


@cli.command()
def paths():
    print(create_general_paths().path)

if __name__ == '__main__':
    cli()

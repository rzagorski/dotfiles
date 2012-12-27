# -*- coding: utf-8 -*-
#!/usr/bin/env python

#pylint: disable=C0103, W0702, R0201, W0621, W1401, R0903, W0232, W0612
'''
Dotfiles organize.
'''

import os
import sys
import subprocess
import shlex

try:
    import argparse
except:
    print "Please upgrade python to 2.7"

directories = []

ignore_files = ['.DS_Store']

class Actions(argparse.Action):
    '''
    Base class for all automated stuff.
    '''

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)
        self.run(namespace)

    def run(self, namespace):
        '''
        Default method run after action is initiated.
        '''
        pass

class Colors:
    '''
    Stupid class with colors for terminal
    From http://stackoverflow.com/questions/287871/print-in-terminal-with-colors-using-python
    '''
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

class Install(Actions):
    '''
    Install stuff
    '''

    def run(self, namespace):
        what_to_do = namespace.install[0]
        directories.insert(0, os.path.abspath('.'))

        if len(directories) > 0:
            for single_directory in directories:
                if os.path.exists(os.path.abspath(single_directory) + "/install"):
                    sys.path.append(os.path.abspath(single_directory + "/install"))
                else:
                    sys.stdout.write("No dotfiles directory in: %s" % os.path.abspath(single_directory))
                    return False

                try:
                    import manifests as external_manifests
                    reload(external_manifests)

                    self.command(what_to_do, external_manifests, single_directory)

                    sys.path.remove(os.path.abspath(single_directory + "/install"))
                except:
                    sys.stdout.write("Nothing to do here")
    
    def command(self, what_to_do, module, single_directory):
        '''
        Execute command
        '''

        if what_to_do == "all" and len(module.manifests):
            sys.stdout.write("Packages from directory: ")
            sys.stdout.write(Colors.HEADER)
            sys.stdout.write(os.path.abspath(single_directory))
            sys.stdout.write(Colors.ENDC)
            sys.stdout.write("\n")
            sys.stdout.flush()
            self.install(module)
        elif what_to_do == "list":
            self.list(module)
        else:
            self.install(module, what_to_do)


    def install(self, install, package_name = None):
        '''
        Install packages. Single or all from manifests.
        '''

        if package_name is None:
            for single_manifest in install.manifests:
                self.install_single_package(single_manifest)
        else:
            for single_manifest in install.manifests:
                if single_manifest['name'] == package_name:
                    self.install_single_package(single_manifest)
                
    def install_single_package(self, single_package):
        '''
        Install single package
        '''

        if 'check' not in single_package:
            single_package['check'] = single_package['name']
        
        exists = self.check_manifest(single_package)

        if not exists or ('force' in single_package and single_package['force']):
            print Colors.WARNING + "Installing package %s" % single_package['name'] + Colors.ENDC
            subprocess.call(single_package['install'], shell=True)
            print
        else:
            print Colors.FAIL + "Package exists: %s" % single_package['name'] + Colors.ENDC

    def list(self, module_with_manifests):
        '''
        List all available packages
        '''

        sys.stdout.write(Colors.OKGREEN + "package name" + " "*(20-len("package name")))
        sys.stdout.write(Colors.OKGREEN + "sudo" + " "*(10-len("sudo")))
        sys.stdout.write(Colors.OKGREEN + "force install" + " "*(20-len("force install")))
        sys.stdout.write(Colors.OKGREEN + "install command")
        sys.stdout.write(Colors.ENDC + "\n")
        for single_package in module_with_manifests.manifests:
            sys.stdout.write(Colors.WARNING)
            sys.stdout.write(single_package['name'] + " "*(20-len(single_package['name'])) + Colors.ENDC)
            
            if "sudo" in shlex.split(single_package['install']):
                sys.stdout.write("True" + " "*(10-len("True")))
            else:
                sys.stdout.write("False" + " "*(10-len("False")))

            if "force" in single_package:
                sys.stdout.write(str(single_package['force']) + " "*(20-len(str(single_package['force']))))
            else:
                sys.stdout.write("False" + " "*(20-len("False")))

            sys.stdout.write(single_package['install'])
            sys.stdout.write("\n")
            sys.stdout.flush()


    def check_manifest(self, single_manifest):
        '''
        Check if manifest is already installed
        '''

        paths = os.environ["PATH"].split(os.pathsep)
        for single_path in paths:
            # Check if it is path
            if os.path.exists(single_manifest['check']) and os.path.basename(single_manifest['check']) != single_path:
                return True

            # Check it it is installed program
            if os.path.exists(single_path + "/" + single_manifest['check']):
                return True

        return False

class Symlink(Actions):
    '''
    Create symlinks in $HOME
    '''

    def run(self, namespace):

        what_to_do = namespace.symlink[0]
        # self.command(what_to_do, os.path.abspath('./symlinks/'))
        directories.insert(0, os.path.abspath('.'))

        if len(directories) > 0:
            for single_directory in directories:
                self.command(what_to_do, os.path.abspath(single_directory) + "/symlinks")

    def command(self, what_to_do, single_directory):
        '''
        Execute command
        '''
        if what_to_do == "all" and os.path.exists(os.path.abspath(single_directory)):
            sys.stdout.write("Files from directory: ")
            sys.stdout.write(Colors.HEADER)
            sys.stdout.write(os.path.abspath(single_directory) + "/symlinks")
            sys.stdout.write(Colors.ENDC)
            sys.stdout.write("\n")
            sys.stdout.flush()

            self.symlink(single_directory)
        elif what_to_do == "list":
            self.list(single_directory)
        else:
            self.symlink(single_directory, what_to_do)

    def list(self, single_directory):
        '''
        List all filest to symlink
        '''
        sys.stdout.write("\n")
        sys.stdout.write(Colors.HEADER)
        sys.stdout.write("file name" + " "*(20-len("file name")))
        sys.stdout.write("installed" + " "*(20-len("installed")))
        sys.stdout.write(Colors.ENDC)
        sys.stdout.write("\n")
        sys.stdout.flush()

        for single_symlink in os.listdir(single_directory):
            if single_symlink in ignore_files:
                continue

            sys.stdout.write(Colors.WARNING)
            sys.stdout.write(single_symlink + " "*(20-len(single_symlink)))
            sys.stdout.write(Colors.ENDC)

            symlink_check = "%s/.%s" % (os.environ['HOME'], single_symlink)
            if os.path.exists(symlink_check) and not os.path.lexists(symlink_check):
                sys.stdout.write("Broken")
            elif os.path.exists(symlink_check):
                sys.stdout.write("True")
            else:
                sys.stdout.write("False")

            sys.stdout.write("\n")
            sys.stdout.flush()

    def symlink(self, single_directory, symlink_name = None):
        '''
        Install packages. Single or all from manifests.
        '''
        if symlink_name is None:
            for single_symlink in os.listdir(single_directory):
                if single_symlink in ignore_files:
                    continue

                self.symlink_single_file("%s/%s" % (single_directory, single_symlink), single_symlink)
        else:
            for single_symlink in os.listdir(single_directory):
                if single_symlink in ignore_files:
                    continue
                    
                if single_symlink == symlink_name:
                    self.symlink_single_file("%s/%s" % (single_directory, single_symlink), single_symlink)
                
    def symlink_single_file(self, single_file_symlink, symlink_name):
        '''
        Install single package
        '''
        symlink_dest = "%s/.%s" % (os.environ['HOME'], symlink_name)
        exists = self.check_symlink(symlink_dest)

        if not exists:
            sys.stdout.write("Creating symlink for: %s \n" % symlink_name)
            os.symlink(single_file_symlink, symlink_dest)
        else:
            pass

    def check_symlink(self, symlink):
        '''
        Check if symlink exists and if it's broken
        '''
        if os.path.exists(symlink):
            return True

        if not os.path.lexists(symlink) and os.path.exists(symlink):
            os.unlink(symlink)

        return False

# class Move(Actions):
#     '''
#     Move stuff
#     '''

#     def run(self, namespace):
#         pass

class Directories(Actions):
    '''
    Add directories
    '''

    def run(self, namespace):
        '''
        Global interface to run things
        '''
        for directory in namespace.directories:
            if os.path.isdir(directory):
                directories.append(directory)


if __name__ == '__main__':
    parser = argparse.ArgumentParser( epilog="""Please do not use '=' after directories option""", 
        usage="%(prog)s [options]")

    parser.add_argument('--directories', nargs='*', help='Append files', metavar='DIR', 
        dest='directories', action=Directories)
    parser.add_argument('--install', nargs=1, help='all, list or _package_', dest='install', action=Install)
    parser.add_argument('--symlink', nargs=1, help='all, list or _file_', dest='symlink', action=Symlink)
    # parser.add_argument('--move', nargs=1, help='all, list or _file_/_directory_', dest='move')

    (options, args) = parser.parse_known_args()
    
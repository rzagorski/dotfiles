import os


class GeneralPaths:

    """
    docstring for GeneralPaths
    """

    PYTHON_VERSIONS = [
        '2.7',
        '3.4',
        '3.5'
    ]

    def __init__(self, paths_behaviours):
        self.paths = os.environ['PATH'].split(':')

        self._paths_behaviours = paths_behaviours

    def create_paths(self):
        """
        Do all the magic and create PATH string
        """

        for behaviour in self._paths_behaviours:
            self.paths = behaviour.add_paths(self.paths).paths

        self._add_dotfiles_bin_path()

    @property
    def path(self):
        """
        Return PATH formatted string
        """

        return ':'.join(self.paths)

    def _add_dotfiles_bin_path(self):
        """
        Add dotfiles bin directory
        """

        user_home = os.path.expanduser('~')
        dotfiles_bin_path = os.path.join(user_home, '.dotfiles/bin')
        if dotfiles_bin_path not in self.paths:
            self.paths.append(
                dotfiles_bin_path
            )

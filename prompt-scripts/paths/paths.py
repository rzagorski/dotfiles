import abc

class Paths(metaclass=abc.ABCMeta):

    """
    Interface for additional paths objects. This can be changed for behaviours based on OS type.
    """

    @abc.abstractmethod
    def add_paths(self, paths_list):
        """
        Add paths to current paths list

        :param list paths_list        : Campaign

        :rtype: None
        """

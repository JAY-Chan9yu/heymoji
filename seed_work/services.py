from abc import ABCMeta


class GenericService(metaclass=ABCMeta):
    repository = None

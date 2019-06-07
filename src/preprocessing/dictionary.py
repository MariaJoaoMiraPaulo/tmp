from .utils import load_dict

class Dictionary:
    """ Equivalent of a singleton Class """

    _instance = None

    def __init__(self):
        if Dictionary._instance is not None:
            pass
        else:
            Dictionary._instance = load_dict()

    @staticmethod
    def get_instance():
        if Dictionary._instance is None:
            Dictionary()
        return Dictionary._instance

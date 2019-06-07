from .utils import load_model

class Model:
    """ Equivalent of a singleton Class """

    _instance = None

    def __init__(self):
        if Model._instance is not None:
            pass
        else:
            Model._instance = load_model()

    @staticmethod
    def get_instance():
        if Model._instance is None:
            Model()
        return Model._instance

from .utils import load_pt_lemmas

class LemmasPt:
    """ Equivalent of a singleton Class """

    _instance = None

    def __init__(self):
        if LemmasPt._instance is not None:
            pass
        else:
            LemmasPt._instance = load_pt_lemmas("./preprocessing/pt_lemmas/lemma_pairs.csv")

    @staticmethod
    def get_instance():
        if LemmasPt._instance is None:
            LemmasPt()
        return LemmasPt._instance

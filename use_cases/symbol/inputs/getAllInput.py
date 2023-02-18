class GetAllInput:
    all :str = None
    base: str = None


    def __init__(self, all=None , base = None):
        self.all = all
        self.base = base
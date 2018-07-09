class Params:

    def __init__(self, id, Wb1, Wb2, Wb1_contaminated, Wb2_contaminated):
        self.id = id
        self.Wb1 = Wb1
        self.Wb2 = Wb2
        self.Wb1_contaminated = Wb1_contaminated
        self.Wb2_contaminated = Wb2_contaminated


class Wb:

    def __init__(self, W, b):
        self.W = W
        self.b = b

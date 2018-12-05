class AddingFilter:
    def __init__(self, stock):
        self._stock = stock
        pass

    def adding(self):
        return 0.000001

    def filterout(self, stock):
        return True

class NodeData:

    def __init__(self, ide, pos):
        self.ide = ide
        self.pos = pos

    def getId(self):
        return self.ide

    def getPos(self):
        return self.pos

    def setPos(self, x, y):
        self.pos = (x, y)

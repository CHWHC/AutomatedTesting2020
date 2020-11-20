class component(object):
    def __init__(self, bounds, component_class,pointer, parent):
        self.bounds = bounds
        self.pointer=pointer
        self.component_class = component_class
        self.parent = parent
        self.children = []

    def __eq__(self, other):
        return self.bounds == other.bounds and self.component_class == other.component_class  # 如果两个bounds和class相等则他们相等

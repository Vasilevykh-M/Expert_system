# переменная
class Variable():
    def __init__(self, name, type, Set, value = None, Question="", Main = False):
        self.name = name
        self.value = value
        self.type = type
        self.Question = Question
        self.Main = Main
        self.Set = Set
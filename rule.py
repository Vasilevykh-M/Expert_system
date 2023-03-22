class Rule:
    def __init__(self, name, inputVars, outputVar, expression, value, reason=""):
        self.name = name
        self.inputVar = inputVars
        self.outputVar = outputVar
        self.expression = expression
        self.value = value
        self.reason = reason

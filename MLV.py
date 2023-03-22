from collections import deque


def MLV(ruleList, dictRule, dictVar, dictAnswer, event):
    stackVar = deque()
    var = None
    for i in dictVar:
        if dictVar[i].Main == True:
            var = dictVar[i]
            break

    def F(var):
       if var.Main == True and len(stackVar) == 0 and var.value != None:
           return

       if var.value == None and var.type == "Выводимая":
           for i in ruleList:
               if dictRule[i].outputVar == var.name:
                   for j in dictRule[i].inputVar:
                       if dictVar[j].value == None:
                           stackVar.append(var)
                           var = dictVar[j]
                           F(var)
                           var = stackVar.pop()
                   flagActivateRule = True
                   for j in dictRule[i].expression:
                     if j[1] == "==" and dictVar[j[0]].value != j[2]:
                       flagActivateRule = False
                       break
                     if j[1] == "!=" and dictVar[j[0]].value == j[2]:
                       flagActivateRule = False
                       break
                   if flagActivateRule == True:
                     var.value = dictRule[i].value

       if var.value == None and var.type != "Выводимая":
            event.wait()
            var.value = dictAnswer
            event.clear()
    F(var)
    print(var.value)
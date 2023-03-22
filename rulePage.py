import flet as ft

import rule
import domain
import variable

class ContextDomain(ft.UserControl):
    def __init__(self, dictDomain, UpDate):
        super(ContextDomain, self).__init__()
        self.dictDomain = dictDomain
        self.UpDate = UpDate
        self.valueDomain = []

    def AddOnChange(self, e):
        self.dictDomain[self.Name.value] = domain.Domain(self.Name.value, list(self.valueDomain))
        self.Name.value=""
        self.TextV.value=""
        self.listDomain.options=[]
        self.listDomain.value=""
        self.StrDomainValue.value=""
        self.AddDomain.disabled=True
        self.DeleteDomain.disabled = True
        self.UpDomain.disabled = True
        self.DownDomain.disabled = True
        self.Add.disabled = True
        self.UpDate()
        self.update()

    def AddValueInDomain(self, e):
        self.valueDomain.append(self.TextV.value)
        self.valueDomain = list(self.valueDomain)
        self.listDomain.options = [ft.dropdown.Option(i) for i in self.valueDomain]
        self.StrDomainValue.value = ""
        for i in self.valueDomain:
            self.StrDomainValue.value += " " + i + "\n"
        self.TextV.value = ""
        self.AddDomain.disabled=True
        self.DisableAdd(self)
        self.update()


    def DeleteValueDomain(self, e):
        self.valueDomain.remove(self.listDomain.value)
        self.listDomain.options = [ft.dropdown.Option(i) for i in self.valueDomain]
        self.StrDomainValue.value = ""
        for i in self.valueDomain:
            self.StrDomainValue.value += " " + i + "\n"
        self.DisableAdd(self)
        self.DeleteDomain.disabled=True
        self.UpDomain.disabled=True
        self.DownDomain.disabled=True
        self.update()


    def upD(self, e):
        for i in range(len(self.valueDomain)):
            if self.valueDomain[i] == self.listDomain.value:
                if i == 0:
                    continue
                temp = self.valueDomain[i-1]
                self.valueDomain[i-1] = self.listDomain.value
                self.valueDomain[i] = temp
        self.listDomain.options = [ft.dropdown.Option(i) for i in self.valueDomain]
        self.StrDomainValue.value = ""
        self.listDomain.value = ""
        for i in self.valueDomain:
            self.StrDomainValue.value += " " + i + "\n"
        self.DeleteDomain.disabled=True
        self.UpDomain.disabled=True
        self.DownDomain.disabled=True
        self.update()

    def downD(self, e):
        for i in range(len(self.valueDomain)):
            if self.valueDomain[i] == self.listDomain.value:
                if i == len(self.valueDomain)-1:
                    continue
                temp = self.valueDomain[i+1]
                self.valueDomain[i+1] = self.listDomain.value
                self.valueDomain[i] = temp
        self.listDomain.options = [ft.dropdown.Option(i) for i in self.valueDomain]
        self.StrDomainValue.value = ""
        self.listDomain.value = ""
        for i in self.valueDomain:
            self.StrDomainValue.value += " " + i + "\n"
        self.DeleteDomain.disabled=True
        self.UpDomain.disabled=True
        self.DownDomain.disabled=True
        self.update()


    def DisableAdd(self, e):
        if self.Name.value == "" or self.valueDomain == [] or self.Name.value in self.dictDomain:
            self.Add.disabled = True
        else:
            self.Add.disabled = False
        self.update()


    def onFocusList(self, e):
        if self.LabelValue.value == "":
            self.DeleteDomain.disabled = True
            self.UpDomain.disabled = True
            self.DownDomain.disabled = True
        else:
            self.DeleteDomain.disabled = False
            self.UpDomain.disabled = False
            self.DownDomain.disabled = False
        self.update()

    def onValueDomain(self, e):
        if self.TextV.value == "" or self.TextV.value in self.valueDomain:
            self.AddDomain.disabled = True
        else:
            self.AddDomain.disabled = False
        self.update()



    def build(self):
        self.Titile = ft.Text("Контекстное пополнение домена", size = 25)

        self.LabelName = ft.Text("Имя домена:")
        self.Name = ft.TextField(
            hint_text="Имя домена",
            width=200,
            on_change=self.DisableAdd
        )
        self.LabelText = ft.Text("Введите новое значение домена:")
        self.TextV = ft.TextField(hint_text="Значение", width=300, on_change=self.onValueDomain)
        self.AddDomain = ft.IconButton(
                            icon=ft.icons.CREATE_OUTLINED,
                            tooltip="Добавить",
                            on_click=self.AddValueInDomain,
                            disabled=True
                        )

        self.DeleteDomain = ft.IconButton(
            icon=ft.icons.DELETE_OUTLINE,
            tooltip="Удалить",
            on_click=self.DeleteValueDomain,
            disabled=True
        )

        self.UpDomain = ft.IconButton(
            ft.icons.ARROW_CIRCLE_UP,
            tooltip="Вверх",
            on_click=self.upD,
            disabled=True
        )

        self.DownDomain = ft.IconButton(
            ft.icons.ARROW_CIRCLE_DOWN,
            tooltip="Вниз",
            on_click=self.downD,
            disabled=True
        )
        self.LabelValue = ft.Text("Выберите значение домена и Удалите, Повыстье позицию, Понизтье позицию")
        self.listDomain = ft.Dropdown(
            width=300,
        on_change=self.onFocusList)

        self.StrDomainValue = ft.TextField(value = "", multiline=True, disabled=True, width=300)

        self.Add = ft.ElevatedButton(text="Сохранить", disabled=True, on_click=self.AddOnChange)

        return ft.Column(controls = [self.Titile, self.LabelName, self.Name, self.LabelText, ft.Row(controls=[self.TextV, self.AddDomain]), self.LabelValue, ft.Row(controls=[self.listDomain, self.UpDomain, self.DownDomain, self.DeleteDomain]), self.StrDomainValue, self.Add])#, ft.Row(controls=[self.Text, self.AddD, self.DeleteD]), self.listDomain, self.Add])

class ContextVar(ft.UserControl):
    def __init__(self, dictVar, dictDomain):
        super(ContextVar, self).__init__()
        self.dictVar = dictVar
        self.dictDomain = dictDomain

    def AddOnChange(self, e):
        self.dictVar[self.Name.value] = variable.Variable(self.Name.value, self.Type.value, self.Set.value, Question=self.Question.value)
        self.Name.value = ""
        self.Type.value= ""
        self.Set.value = ""
        self.Question.value = ""
        self.Add.disabled = True
        self.update()

    def onFocusType(self, e):
        if self.Type.value == "Запрашиваемая" or self.Type.value =="Выводимо/Запрашиваемая":
            self.LabelQuestion.visible = True
            self.Question.visible = True
        else:
            self.LabelQuestion.visible = False
            self.Question.visible = False

        self.onValid(self)
        self.update()

    def onValid(self, e):
        if self.Name.value == "":
            self.Type.disabled = True
            self.Set.disabled = True
        else:
            self.Type.disabled = False
            self.Set.disabled = False

        if self.Name.value == "" or self.Type.value == "" or self.Set.value == "" or self.Name.value in self.dictVar:
            self.Add.disabled = True
        else:
            self.Add.disabled = False

        self.Question.value = self.Name.value + "?"
        self.update()

    def UpDate(self):
        self.Set.options = [ft.dropdown.Option(i) for i in self.dictDomain]
        self.update()

    def build(self):
        self.Titile = ft.Text("Контекстное пополнение переменной", size = 25)
        self.LabelName = ft.Text("Имя перменной:")
        self.Name = ft.TextField(
            hint_text="Имя переменной",
            width=400,
            on_change=self.onValid
        )
        self.LabelType = ft.Text("Тип перменной")
        self.Type = ft.Dropdown(
            width=400,
            options=[
                ft.dropdown.Option("Запрашиваемая"),
                ft.dropdown.Option("Выводимая"),
                ft.dropdown.Option("Выводимо/Запрашиваемая")
            ],
            disabled=True if self.Name.value == "" else False,
            on_change=self.onFocusType
        )
        self.LabelSet = ft.Text("Множество значений")
        self.Set = ft.Dropdown(
            hint_text="Множество значений",
            width=400,
            disabled=True if self.Name.value == "" else False,
            options=[ft.dropdown.Option(i) for i in self.dictDomain],
            on_change=self.onValid
        )
        self.LabelQuestion = ft.Text("Вопрос", visible=False)
        self.Question = ft.TextField(
            hint_text="Вопрос",
            width=300,
            visible=False,
            value=self.dictVar[self.Name.value].Question if self.Name.value in self.dictVar else self.Name.value + "?",
        )
        self.Add = ft.ElevatedButton(text="Сохранить", disabled=True if self.Name.value == "" else False, on_click=self.AddOnChange)

        return ft.Column(controls = [self.Titile, self.LabelName, self.Name, self.LabelType, self.Type, self.LabelSet, self.Set, self.LabelQuestion, self.Question, self.Add])


class Var(ft.UserControl):
    def __init__(self, deleteVar, addVar, dictVar, dictRule, listRule, dictDomain, name = "", mod = False, position = -1):
        super(Var, self).__init__()
        self.deleteVar = deleteVar
        self.addVar = addVar
        self.dictVar = dictVar
        self.dictRule = dictRule
        self.listRule = listRule
        self.dictDomain = dictDomain
        self.name = name
        self.mod = mod
        self.ListInputVar = dictRule[name].inputVar if name in dictRule else []
        self.OutputVar = dictRule[name].outputVar if name in dictRule else ""
        self.Expression = dictRule[name].expression if name in dictRule else []
        self.value = dictRule[name].value if name in dictRule else ""
        self.index = position
        self.index1 = -1


    def AddRule(self, e):
        self.dictRule[self.name] = rule.Rule(self.name, self.ListInputVar, self.OutputVar, self.Expression, self.value, self.Reason)
        print(self.listRule)
        print(self.index)
        if self.index == -1:
            self.listRule.append(self.name)
        else:
            self.listRule[self.index] = self.name
        self.addVar(self.name, mod = self.mod)
        self.deleteVar(self)

    def getStrPremise(self):
        strPremise = ""
        for i in range(len(self.Expression)):
            expression = self.Expression[i][0] + " " \
                             +  self.Expression[i][1] + " "\
                             +  self.Expression[i][2]
            if i == 0:
                strPremise = expression
            else:
                strPremise += " И " + expression
        return strPremise

    def getInputVars(self):
        return [ft.dropdown.Option(i) for i in [self.dictVar[i].name for i in self.dictVar if i != self.OutputVar]]

    def onVarSelect(self, e):
        nameVar = self.PremiseVar.value
        self.ValueInputPremise.options = [ft.dropdown.Option(i) for i in self.dictDomain[self.dictVar[nameVar].Set].set]
        self.validationPermisionInputField(self)
        self.update()

    def addExpression(self, e):
        if self.index1 == -1:
            nameVar = self.PremiseVar.value
            sign = self.Sign.value
            value = self.ValueInputPremise.value
            self.Expression.append((nameVar, sign, value))
            self.PremiseVar.value = None
            self.Sign.value = None
            self.ValueInputPremise.value = None
            self.ListPremise.value = "Посылка: " + self.getStrPremise()
            self.ListInputVar.append(nameVar)
            self.AddPremise1.disabled = True
            self.AddPremise2.disabled = True
            self.validAddRule(self)
            self.initListBoxPremise()
            self.initOutputVar()
        else:
            nameVar = self.PremiseVar.value
            sign = self.Sign.value
            value = self.ValueInputPremise.value
            self.Expression[self.index1] = (nameVar, sign, value)
            self.PremiseVar.value = None
            self.Sign.value = None
            self.ValueInputPremise.value = None
            self.ListPremise.value = "Посылка: " + self.getStrPremise()
            self.AddPremise1.disabled = True
            self.AddPremise2.disabled = True
            self.validAddRule(self)
            self.initListBoxPremise()
            self.initOutputVar()

        self.AddPremise2.visible = False
        self.AddPremise1.visible = True

        self.update()

    def editExpression(self, e):
        v = self.splitValue()
        value = (v[0], v[1], v[2])
        for i in range(len(self.Expression)):
            print(self.Expression[i])
            print(value)
            if self.Expression[i] == value:
                self.PremiseVar.value = value[0]
                self.Sign.value = value[1]
                self.ValueInputPremise.options = [ft.dropdown.Option(j) for j in self.dictDomain[self.dictVar[value[0]].Set].set]
                self.ValueInputPremise.value = value[2]
                self.index1 = i
                self.AddPremise1.disabled = False
                self.AddPremise2.disabled = False
                break
        self.AddPremise2.visible = True
        self.AddPremise1.visible = False
        self.update()

    def initListBoxPremise(self):
        self.ListBoxPremise.options=[ft.dropdown.Option(i[0]+" "+i[1]+" "+i[2]) for i in self.Expression]
        self.update()

    def splitValue(self):
        i = 0
        v = ["", "", ""]
        while self.ListBoxPremise.value[i] != '=' and self.ListBoxPremise.value[i] != '!':
            v[0] += self.ListBoxPremise.value[i]
            i += 1
        v[0] = v[0][:-1]
        v[1] = self.ListBoxPremise.value[i] + self.ListBoxPremise.value[i + 1]
        i += 2
        while i < len(self.ListBoxPremise.value):
            v[2] += self.ListBoxPremise.value[i]
            i += 1
        v[2] = v[2][1:]
        return v

    def removeValueInListBoxPremise(self, e):
        value = self.splitValue()
        self.Expression.remove((value[0], value[1], value[2]))
        self.ListPremise.value = "Посылка: " + self.getStrPremise()
        self.ListInputVar.remove(value[0])
        self.DeletePremise.disabled = True
        self.validAddRule(self)
        self.initListBoxPremise()
        self.initOutputVar()
        self.update()

    def initOutputVar(self):
        self.outputVar.options = []
        for i in self.dictVar:
            if (not i in self.ListInputVar) and self.dictVar[i].type != "Запрашиваемая":
                self.outputVar.options.append(ft.dropdown.Option(i))
        self.update()

    def onSelectOutputVar(self, e):
        varName = self.outputVar.value
        self.OutputVar = varName
        self.PremiseVar.options = self.getInputVars()
        self.ValueInput.options = [ft.dropdown.Option(i) for i in self.dictDomain[self.dictVar[varName].Set].set]
        self.update()

    def validationPermisionInputField(self, e):
        if self.PremiseVar.value != None and self.Sign.value != None and self.ValueInputPremise.value != None:
            self.AddPremise1.disabled = False
            self.AddPremise2.disabled = False
        else:
            self.AddPremise1.disabled = True
            self.AddPremise2.disabled = True
        self.update()

    def validationDeletePermision(self, e):
        if self.ListBoxPremise.value == None:
            self.DeletePremise.disabled = True
            self.EditPremise.disabled = True
        else:
            self.DeletePremise.disabled = False
            self.EditPremise.disabled = False
        self.update()

    def validAddButton(self):
        name = self.Name.value != "" and self.Name.value != None and not self.Name.value is self.dictRule
        expression = self.ListInputVar != [] and self.Expression != []
        value = self.value != "" and self.value != None
        return name and expression and value

    def validAddRule(self, e):
        self.name = self.Name.value
        if self.validAddButton():
            self.AddRule.disabled = False
        else:
            self.AddRule.disabled = True
        self.update()

    def ValueOnChange(self, e):
        self.value = self.ValueInput.value
        self.validAddRule(self)

    def build(self):
        self.LabelName = ft.Text("Имя правила")
        self.Name = ft.TextField(
            hint_text="Имя правила",
            width=200,
            on_change=self.validAddRule,
            value=self.name
        )

        self.LabelPremise = ft.Text("Посылка")
        self.PremiseVar = ft.Dropdown(
            hint_text="Переменная",
            options=self.getInputVars(),
            on_change=self.onVarSelect,
            text_size=10,
        )

        self.Sign = ft.Dropdown(
            hint_text="Выражение",
            options=[ft.dropdown.Option("=="), ft.dropdown.Option("!=")],
            on_change=self.validationPermisionInputField,
            text_size=10,
        )

        self.ValueInputPremise = ft.Dropdown(
            hint_text="Значение",
            options=[],
            on_change=self.validationPermisionInputField,
            text_size=10,
        )

        self.AddPremise1 = ft.IconButton(
            icon=ft.icons.ADD,
            tooltip="Добавить",
            on_click=self.addExpression,
            disabled=True
        )

        self.AddPremise2 = ft.IconButton(
            icon=ft.icons.CREATE_OUTLINED,
            tooltip="Изменить",
            on_click=self.addExpression,
            disabled=True,
            visible=False
        )


        self.ListPremise = ft.Text("Посылка: " + self.getStrPremise())

        self.LabelListBoxPremise = ft.Text("Выберите посылку для удаления")
        self.ListBoxPremise = ft.Dropdown(
            hint_text="Посылки",
            options=[ft.dropdown.Option(i[0]+" "+i[1]+" "+i[2]) for i in self.Expression],
            on_change=self.validationDeletePermision,
            text_size=10,
        )

        self.DeletePremise = ft.IconButton(
            ft.icons.DELETE_OUTLINE,
            tooltip="Удалить",
            on_click=self.removeValueInListBoxPremise,
            disabled=True
        )

        self.EditPremise = ft.IconButton(
            icon=ft.icons.CREATE_OUTLINED,
            tooltip="Изменить",
            on_click=self.editExpression,
            disabled=True
        )

        self.LabelOutput = ft.Text("Выходная переменная")

        self.outputVar = ft.Dropdown(
            hint_text="Переменная",
            options= [ft.dropdown.Option(i) for i in self.dictVar if not i in self.ListInputVar and self.dictVar[i].type != "Запрашиваемая"],
            on_change=self.onSelectOutputVar,
            value=self.OutputVar,
            text_size=10,
        )

        self.ValueInput = ft.Dropdown(
            hint_text="Значение",
            options=[ft.dropdown.Option(i) for i in self.dictDomain[self.dictVar[self.OutputVar].Set].set] if self.OutputVar in self.dictVar and  self.outputVar.options != [] else [],
            on_change=self.ValueOnChange,
            value=self.value,
            text_size=10,
        )

        self.ValueInput.value = self.value
        print(self.OutputVar in self.dictDomain)

        self.LabelReason = ft.Text("Объяснение")
        self.Reason = ft.TextField(value= (self.dictRule[self.name].reason if self.name !="" else ""))

        self.AddRule = ft.ElevatedButton(text="Сохранить", disabled= False if self.validAddButton() else True, on_click=self.AddRule)



        return ft.Column(controls = [self.LabelName, self.Name,
                                     self.LabelPremise,
                                     ft.Row(controls=[self.PremiseVar, self.Sign, self.ValueInputPremise, self.AddPremise1,self.AddPremise2]),
                                     self.ListPremise,
                                     self.LabelListBoxPremise,
                                     ft.Row(controls=[self.ListBoxPremise, self.DeletePremise, self.EditPremise]),
                                     self.LabelOutput,
                                     ft.Row(controls=[self.outputVar, self.ValueInput]),
                                     self.LabelReason,
                                     self.Reason,
                                     self.AddRule])


class Variab(ft.UserControl):
    def __init__(self, varName, deleteVar, dictRule, add_clicked, listRule, reBuild, expr, outputVar, value):
        super().__init__()
        self.varName = varName
        self.deleteVar = deleteVar
        self.dictRule = dictRule
        self.add_clicked = add_clicked
        self.listRule = listRule
        self.reBuild = reBuild
        self.expr = expr
        self.outputVar = outputVar
        self.value = value

    def DelOnClick(self, e):
        self.dictRule.pop(self.varName)
        self.listRule.remove(self.varName)
        self.deleteVar(self)

    def modVar(self, e):
        pos = 0
        self.visible = False
        for i in range(len(self.listRule)):
            if self.listRule[i] == self.varName:
                pos = i
        self.add_clicked(self, self.varName)
        self.dictRule.pop(self.varName)
        self.deleteVar(self)
        self.update()

    def upRule(self, e):
        for i in range(len(self.listRule)):
            if self.listRule[i] == self.varName:
                if i == 0:
                    return
                temp = self.listRule[i-1]
                self.listRule[i-1] = self.varName
                self.listRule[i] = temp
                self.reBuild()
                return

    def downRule(self, e):
        for i in range(len(self.listRule)):
            if self.listRule[i] == self.varName:
                if i == len(self.listRule)-1:
                    return
                temp = self.listRule[i+1]
                self.listRule[i+1] = self.varName
                self.listRule[i] = temp
                self.reBuild()
                return


    def build(self):
        self.exprT = ft.Text("IF: ", size = 10, weight=ft.FontWeight.BOLD)
        for i in range(len(self.expr)):
            if i == 0:
                self.exprT.value += self.expr[i][0] + self.expr[i][1] + self.expr[i][2]
            else:
                self.exprT.value += " И " + self.expr[i][0] + self.expr[i][1] + self.expr[i][2]
        self.exprT.value += " Then " + self.outputVar + " = "+ self.value

        self.display_view = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(self.varName, size = 10, weight=ft.FontWeight.BOLD),
                self.exprT,
                ft.Row(
                    spacing=0,
                    controls=[
                        ft.IconButton(
                            icon=ft.icons.CREATE_OUTLINED,
                            tooltip="Изменить",
                            on_click=self.modVar,
                        ),
                        ft.IconButton(
                            ft.icons.DELETE_OUTLINE,
                            tooltip="Удалить",
                            on_click=self.DelOnClick,
                        ),
                        ft.IconButton(
                            ft.icons.ARROW_CIRCLE_UP,
                            tooltip="Вверх",
                            on_click=self.upRule,
                        ),
                        ft.IconButton(
                            ft.icons.ARROW_CIRCLE_DOWN,
                            tooltip="Вниз",
                            on_click=self.downRule,
                        )
                    ],
                ),
            ],
        )
        return ft.Column(controls=[self.display_view])


class ListRule(ft.UserControl):

    def __init__(self, dictVar, dictRule, listRule, dictDomain):
        super(ListRule, self).__init__()
        self.dictVar = dictVar
        self.dictRule = dictRule
        self.listRule = listRule
        self.dictDomain = dictDomain

    def add_clicked(self, e, name = "", position = -1, mod = True):
        print("Edit")

        for i in range(len(self.vars.controls)):
            if self.vars.controls[i].varName == name:
                position = i

        var = Var(self.ruleDelete, self.addRule, self.dictVar, self.dictRule, self.listRule, self.dictDomain, name, mod, position)

        if position == -1:
            self.vars.controls.insert(0, var)
        else:
            self.vars.controls[position] = var
        self.update()

    def AddRule(self, name = ""):
        print(name)
        var = Var(self.ruleDelete, self.addRule, self.dictVar, self.dictRule, self.listRule, self.dictDomain, "", False)
        self.vars.controls.insert(0, var)
        self.update()

    def addRule(self, name, position = -1, mod = False):

        print("Add")

        for i in range(len(self.vars.controls)):
            if isinstance(self.vars.controls[i], Var) and self.vars.controls[i].name == name and mod == True:
                position = i
        if position == -1:
            self.vars.controls.append(Variab(
                    name,
                    self.ruleDelete,
                    self.dictRule,
                    self.add_clicked,
                    self.listRule,
                    self.reBuild,
                    self.dictRule[name].expression,
                    self.dictRule[name].outputVar,
                    self.dictRule[name].value
                )
            )
        else:
            self.vars.controls[position] =  Variab(
                    name,
                    self.ruleDelete,
                    self.dictRule,
                    self.add_clicked,
                    self.listRule,
                    self.reBuild,
                    self.dictRule[name].expression,
                    self.dictRule[name].outputVar,
                    self.dictRule[name].value
                )

        print(self.listRule)
        self.update()

    def ruleDelete(self, var):
        self.vars.controls.remove(var)
        self.update()

    def reBuild(self):
        self.vars.controls = [
            Variab(
                i,
                self.ruleDelete,
                self.dictRule,
                self.add_clicked,
                self.listRule,
                self.reBuild,
                self.dictRule[i].expression,
                self.dictRule[i].outputVar,
                self.dictRule[i].value,
            ) for i in self.listRule]
        self.update()

    def on_click_context_menu(self, e):
        self.var.visible = not self.var.visible
        self.domain.visible = not self.domain.visible
        self.context_menu.text = "Отобразить контекстное меню" if self.context_menu.text == "Скрыть контекстное меню" else "Скрыть контекстное меню"
        self.update()


    def build(self):
        self.newVar = ft.ElevatedButton(text="Создать", disabled=False, on_click=self.AddRule)
        self.var = ContextVar(self.dictVar, self.dictDomain)
        self.domain = ContextDomain(self.dictDomain, self.var.UpDate)
        self.context_menu = ft.ElevatedButton(text="Скрыть контекстное меню", on_click=self.on_click_context_menu)
        self.vars = ft.Column([
            Variab(
                i,
                self.ruleDelete,
                self.dictRule,
                self.add_clicked,
                self.listRule,
                self.reBuild,
                self.dictRule[i].expression,
                self.dictRule[i].outputVar,
                self.dictRule[i].value,
            ) for i in self.listRule])
        return ft.Column(controls=[self.newVar, self.context_menu, ft.Row(controls=[self.domain, self.var]), self.vars])
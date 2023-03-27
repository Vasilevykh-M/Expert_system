import flet as ft

import variable
import domain


class ContextDomain(ft.UserControl):
    def __init__(self, dictDomain, update_domain):
        super(ContextDomain, self).__init__()
        self.dictDomain = dictDomain
        self.valueDomain = []
        self.update_domain = update_domain

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
        self.update_domain()
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


class Var(ft.UserControl):
    def __init__(self, deleteVar, addVar, dictVar, dictDomain, name="", mod = False, position = -1, listVar = []):
        super(Var, self).__init__()
        self.deleteVar = deleteVar
        self.addVar = addVar
        self.dictVar = dictVar
        self.name = name
        self.dictDomain = dictDomain
        self.mod = mod
        self.index = position
        self.listVar = listVar


    def AddOnChange(self, e):
        self.dictVar[self.Name.value] = variable.Variable(self.Name.value, self.Type.value, self.Set.value, Question=self.Question.value)

        if self.index == -1:
            self.listVar.append(self.name)
        else:
            self.listVar[self.index] = self.name
        print(self.dictVar)
        name = self.Name.value
        self.addVar(name, mod = self.mod)
        self.deleteVar(self)

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

    def on_click_context_menu(self, e):
        self.domain.visible = not self.domain.visible
        self.context_menu.text = "Отобразить контекстное меню" if self.context_menu.text == "Скрыть контекстное меню" else "Скрыть контекстное меню"
        self.update()

    def update_domain(self):
        self.Set.options = [ft.dropdown.Option(i) for i in self.dictDomain]
        self.update()

    def build(self):
        self.LabelName = ft.Text("Имя перменной:")
        self.Name = ft.TextField(
            hint_text="Имя переменной",
            width=400,
            value=self.name,
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
            value=self.dictVar[self.name].type if self.name in self.dictVar else "",
            on_change=self.onFocusType
        )
        self.LabelSet = ft.Text("Множество значений")
        self.Set = ft.Dropdown(
            hint_text="Множество значений",
            width=400,
            disabled=True if self.Name.value == "" else False,
            value=self.dictVar[self.name].Set if self.name in self.dictVar else "",
            options=[ft.dropdown.Option(i) for i in self.dictDomain],
            on_change=self.onValid
        )
        self.LabelQuestion = ft.Text("Вопрос", visible=False if self.name == "" else True)
        self.Question = ft.TextField(
            hint_text="Вопрос",
            width=300,
            visible=False if self.name == "" else True,
            value=self.dictVar[self.Name.value].Question if self.Name.value in self.dictVar else self.Name.value + "?",
        )
        self.Add = ft.ElevatedButton(text="Сохранить", disabled=True if self.Name.value == "" else False, on_click=self.AddOnChange)
        self.domain = ContextDomain(self.dictDomain, self.update_domain)
        self.domain.visible=False
        self.context_menu = ft.ElevatedButton(text="Отобразить контекстное меню", on_click=self.on_click_context_menu)
        return ft.Column(controls = [ self.context_menu, self.domain,
            self.LabelName, self.Name, self.LabelType, self.Type, self.LabelSet, self.Set, self.LabelQuestion, self.Question, self.Add])


class Variab(ft.UserControl):
    def __init__(self, varName, deleteVar, dictVar, add_clicked, Main, Build, dictRule, dictDomain, listVar):
        super().__init__()
        self.varName = varName
        self.deleteVar = deleteVar
        self.dictVar = dictVar
        self.add_clicked = add_clicked
        self.Main = Main
        self.Build = Build
        self.dictRule = dictRule
        self.dictDomain = dictDomain
        self.listVar = listVar


    def DelOnClick(self, e):
        self.dictVar.pop(self.varName)
        self.listVar.remove(self.varName)
        self.deleteVar(self)

    def modVar(self, e):

        pos = 0
        self.visible = False
        for i in range(len(self.listVar)):
            if self.listVar[i] == self.varName:
                pos = i
        self.add_clicked(self, self.varName)
        self.dictVar.pop(self.varName)
        self.deleteVar(self)
        self.update()

    def mainVar(self, e):
        for i in self.dictVar:
            self.dictVar[i].Main = False
        self.dictVar[self.varName].Main = True
        self.Build()

    def findVar(self):
        for i in self.dictRule:
            if self.varName in self.dictRule[i].inputVar or self.varName == self.dictRule[i].outputVar:
                return True
        return False


    def build(self):
        self.display_task = ft.Checkbox(value=self.Main, on_change=self.mainVar, disabled=True if self.dictVar[self.varName].type == "Запрашиваемая" else False)    # не работает с radio button
        self.NameRule = ft.Text(value = self.varName, size = 20, weight=ft.FontWeight.BOLD)
        self.domain_name = ft.Text(value="Домен: " + self.dictVar[self.varName].Set)
        self.domain = ft.Dropdown(options=[ft.dropdown.Option(i) for i in self.dictDomain[self.dictVar[self.varName].Set].set], text_size=10)
        list_rule=[]
        for i in self.dictRule:
            if self.varName in self.dictRule[i].inputVar or self.varName == self.dictRule[i].outputVar:
                list_rule.append(i)
        self.rule_label = ft.Text(value="Правила: ")
        self.rule  = ft.Dropdown(options=[ft.dropdown.Option(i) for i in list_rule], text_size=10)
        self.display_view = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.display_task,
                self.NameRule,
                self.domain_name,
                self.domain,
                self.rule_label,
                self.rule,
                ft.Row(
                    spacing=0,
                    controls=[
                        ft.IconButton(
                            icon=ft.icons.CREATE_OUTLINED,
                            tooltip="Изменить",
                            on_click=self.modVar,
                            disabled=self.findVar()
                        ),
                        ft.IconButton(
                            ft.icons.DELETE_OUTLINE,
                            tooltip="Удалить",
                            on_click=self.DelOnClick,
                            disabled=self.findVar()
                        ),
                    ],
                ),
            ],
        )
        return ft.Column(controls=[self.display_view])


class ListVar(ft.UserControl):

    def __init__(self, dictVar, dictDomain, dictRule):
        super(ListVar, self).__init__()
        self.dictVar = dictVar
        self.dictDomain = dictDomain
        self.dictRule = dictRule
        self.listVar=[self.dictVar[i].name for i in dictVar]

    def add_clicked(self, e, name = "", position = -1, mod = True):

        print("Edit")

        for i in range(len(self.vars.controls)):
            if self.vars.controls[i].varName == name:
                position = i

        var = Var(self.varDelete, self.addVar, self.dictVar, self.dictDomain, name, mod, position, self.listVar)

        if position == -1:
            self.vars.controls.insert(0, var)
        else:
            self.vars.controls[position] = var
        self.update()

    def AddRule(self, name = ""):
        print(name)
        var = Var(self.varDelete, self.addVar, self.dictVar, self.dictDomain, "", False, listVar=self.listVar)
        self.vars.controls.insert(0, var)
        self.update()

    def addVar(self, name, position = -1, mod = False):
        print("Add")

        for i in range(len(self.vars.controls)):
            if isinstance(self.vars.controls[i], Var) and self.vars.controls[i].name == name and mod == True:
                position = i
        if position == -1:
            self.vars.controls.append(Variab(
                    name,
                    self.varDelete,
                    self.dictVar,
                    self.add_clicked,
                    self.dictVar[name].Main,
                    self.reBuild,
                    self.dictRule,
                    self.dictDomain,
                    self.listVar
                )
            )
        else:
            self.vars.controls[position] = Variab(
                    name,
                    self.varDelete,
                    self.dictVar,
                    self.add_clicked,
                    self.dictVar[name].Main,
                    self.reBuild,
                    self.dictRule,
                    self.dictDomain,
                    self.listVar
                )

        self.update()


    def varDelete(self, var):
        self.vars.controls.remove(var)
        self.update()

    def reBuild(self):
        self.vars.controls=[Variab(i, self.varDelete, self.dictVar, self.add_clicked, self.dictVar[i].Main, self.reBuild, self.dictRule, self.dictDomain, self.listVar) for i in self.dictVar]
        self.update()

    def build(self):
        self.newVar = ft.ElevatedButton(text="Создать", disabled=False, on_click=self.AddRule)

        self.vars = ft.Column([Variab(i, self.varDelete, self.dictVar, self.add_clicked, self.dictVar[i].Main, self.reBuild, self.dictRule, self.dictDomain, self.listVar) for i in self.dictVar])
        return ft.Column(controls=[self.newVar, self.vars,])
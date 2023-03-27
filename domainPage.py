import flet as ft

import domain

class Var(ft.UserControl):
    def __init__(self, deleteVar, addVar, dictDomain, name="", mod = False, position = -1, listVar = []):
        super(Var, self).__init__()
        self.deleteVar = deleteVar
        self.addVar = addVar
        self.dictDomain = dictDomain
        self.name = name
        self.valueDomain = dictDomain[name].set if name in dictDomain else []
        self.mod = mod
        self.index = position
        self.listVar = listVar


    def AddOnChange(self, e):
        self.dictDomain[self.Name.value] = domain.Domain(self.Name.value, list(self.valueDomain))

        if self.index == -1:
            self.listVar.append(self.name)
        else:
            self.listVar[self.index] = self.name
        print(self.dictDomain)

        name = self.Name.value
        self.addVar(name, mod = self.mod)
        self.deleteVar(self)

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


    def upRule(self, e):
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

    def downRule(self, e):
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
        self.LabelName = ft.Text("Имя домена:")
        self.Name = ft.TextField(
            hint_text="Имя домена",
            width=200,
            value=self.name,
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
            on_click=self.upRule,
            disabled=True
        )

        self.DownDomain = ft.IconButton(
            ft.icons.ARROW_CIRCLE_DOWN,
            tooltip="Вниз",
            on_click=self.downRule,
            disabled=True
        )
        self.LabelValue = ft.Text("Выберите значение домена и Удалите, Повыстье позицию, Понизтье позицию")
        self.listDomain = ft.Dropdown(
            options= [ft.dropdown.Option(i) for i in list(self.dictDomain[self.name].set)] if self.name in self.dictDomain else [],
            width=300,
        on_change=self.onFocusList)

        self.StrDomainValue = ft.TextField(value = "", multiline=True, disabled=True, width=300)
        if self.name in self.dictDomain:
            for i in list(self.dictDomain[self.name].set):
                self.StrDomainValue.value+=" " + i + "\n"


        self.Add = ft.ElevatedButton(text="Сохранить", disabled=True if self.Name.value == "" else False, on_click=self.AddOnChange)

        return ft.Column(controls = [self.LabelName, self.Name, self.LabelText, ft.Row(controls=[self.TextV, self.AddDomain]), self.LabelValue, ft.Row(controls=[self.listDomain, self.UpDomain, self.DownDomain, self.DeleteDomain]), self.StrDomainValue, self.Add])#, ft.Row(controls=[self.Text, self.AddD, self.DeleteD]), self.listDomain, self.Add])


class Variab(ft.UserControl):
    def __init__(self, varName, deleteVar, dictDomain, add_clicked, listVar):
        super().__init__()
        self.varName = varName
        self.deleteVar = deleteVar
        self.dictDomain = dictDomain
        self.add_clicked = add_clicked
        self.listVar = listVar

    def DelOnClick(self, e):
        self.dictDomain.pop(self.varName)
        self.listVar.remove(self.varName)
        self.deleteVar(self)

    def modVar(self, e):
        pos = 0
        self.visible = False
        for i in range(len(self.listVar)):
            if self.listVar[i] == self.varName:
                pos = i
        self.add_clicked(self, self.varName)
        self.dictDomain.pop(self.varName)
        self.deleteVar(self)
        self.update()


    def build(self):
        self.dictValue = ft.Dropdown(value="", options=[])
        if self.varName in self.dictDomain:
            self.dictValue.options=[ft.dropdown.Option(i) for i in list(self.dictDomain[self.varName].set)]

        self.display_view = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(value=self.varName, size = 20, weight=ft.FontWeight.BOLD),
                ft.Text(value="Значения домена: "),
                self.dictValue,
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
                    ],
                ),
            ],
        )

        return ft.Column(controls=[self.display_view])


class ListDomain(ft.UserControl):

    def __init__(self, dictDomain):
        super(ListDomain, self).__init__()
        self.dictDomain = dictDomain
        self.listVar = [self.dictDomain[i].name for i in dictDomain]

    def add_clicked(self, e, name = "", position = -1, mod = True):

        print("Edit")

        for i in range(len(self.vars.controls)):
            if self.vars.controls[i].varName == name:
                position = i

        var = Var(self.varDelete, self.addVar, self.dictDomain, name, mod, position, self.listVar)

        if position == -1:
            self.vars.controls.insert(0, var)
        else:
            self.vars.controls[position] = var
        self.update()

    def AddRule(self, name = ""):
        print(name)
        var =Var(self.varDelete, self.addVar, self.dictDomain, "", False, listVar=self.listVar)
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
                    self.dictDomain,
                    self.add_clicked,
                    self.listVar
                )
            )
        else:
            self.vars.controls[position] = Variab(
                    name,
                    self.varDelete,
                    self.dictDomain,
                    self.add_clicked,
                    self.listVar
            )

        self.update()

    def varDelete(self, var):
        self.vars.controls.remove(var)
        self.update()

    def build(self):

        self.newVar = ft.ElevatedButton(text="Создать", disabled=False, on_click=self.AddRule)
        self.vars = ft.Column([Variab(i, self.varDelete, self.dictDomain, self.add_clicked, self.listVar) for i in self.dictDomain])
        return ft.Column(controls=[self.newVar, self.vars,])
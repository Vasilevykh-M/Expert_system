import pickle
import threading
import time
from collections import deque


import flet as ft

import rule
import variable
import domain
import logs

class mainPage(ft.UserControl):

    def __init__(self):
        super(mainPage, self).__init__()
        self.dictRule = {}
        self.dictVar = {}
        self.listRule = {"listRule": []}
        self.dictDomain = {}
        self.dictAnswer = {"Answer": ""}
        self.varValue=[]
        self.treeView = []
        self.event = threading.Event()
        self.ThreadMLV = threading.Thread(name ="MLV", target=self.MLV)
        self.file_name = ""
        self.ThreadMLV.start()

    def OnLoadResult(self, e: ft.FilePickerResultEvent):
        if e.files != None:
            with open(e.files[0].path, 'rb') as file:
                obj = pickle.load(file)
                self.file_name = e.files[0].path

            for i in obj["dictDomain"]:
                self.dictDomain[i["name"]] = domain.Domain(i["name"], set(i["set"]))

            for i in obj["dictVar"]:
                self.dictVar[i["name"]] = variable.Variable(i["name"], i["type"], i["Set"], Question=i["Question"], Main=i["Main"])

            for i in obj["dictRule"]:
                l = []
                for j in i["expression"]:
                    l.append((j[0], j[1], j[2]))

                self.dictRule[i["name"]] = rule.Rule(i["name"], i["inputVar"], i["outputVar"], l, i["value"])

            self.listRule["listRule"] = obj["listRule"]
            self.event.set()

    def MLV(self):
        self.event.wait()
        self.event.clear()
        time.sleep(2)
        stackVar = deque()
        var = None
        for i in self.dictVar:
            if self.dictVar[i].Main == True:
                var = self.dictVar[i]
                break


        def F(var, depth):
            if var != None and var.value != None and var.Main == True and len(stackVar) == 0:
                return

            if var.value == None and var.type != "Запрашиваемая":
                for i in self.listRule["listRule"]:
                    if self.dictRule[i].outputVar == var.name:
                        flagActivateRule = True
                        for j in self.dictRule[i].expression:
                            if self.dictVar[j[0]].value == None:
                                stackVar.append(var)
                                var = self.dictVar[j[0]]
                                F(var, depth + 1)
                                var = stackVar.pop()

                            if j[1] == "==" and self.dictVar[j[0]].value != j[2]:
                                flagActivateRule = False
                                break

                            if j[1] == "!=" and self.dictVar[j[0]].value == j[2]:
                                flagActivateRule = False
                                break
                        if flagActivateRule == True:
                            var.value = self.dictRule[i].value
                            self.varValue.append((var.name, var.value))
                            self.treeView.append({"name": self.dictRule[i].name, "depth": depth, "child": []})
                            break

            if var.value == None and var.type != "Выводимая":
                self.cretateQuestion(var)
                self.event.wait()
                var.value = self.dictAnswer["Answer"]
                self.dictVar[var.name].value = self.dictAnswer["Answer"]
                self.varValue.append((var.name, var.value))
                self.event.clear()
        if var == None:
            self.er()
            print("A")
        else:
            F(var, 0)
            self.printAnswer(var)

    def find1(self, arr, name):
        for x in arr:
            if x["name"] == name:
                return x


    def r(self, dict_):
        dict_.reverse()
        for i in range(len(dict_)):
            for j in range(i + 1, len(dict_)):
                if dict_[i]["depth"] >= dict_[j]["depth"]:
                    break
                if dict_[i]["depth"] + 1 == dict_[j]["depth"]:
                    dict_[i]["child"].append(dict_[j]["name"])
            dict_[i]["child"].reverse()
        return dict_

    def print_val(self, obj, dict_):
        self.text.value += self.print_ans(obj)
        child = obj["child"]
        dict_.remove(obj)
        for i in child:
            self.print_val(self.find1(dict_, i), dict_)

    def print_ans(self, obj):
        valueText = ""
        for j in range(obj["depth"]):
            valueText += "     "
        expr = "IF "
        for j in self.dictRule[obj["name"]].expression:
            expr += j[0] + " " + j[1] + " " + j[2] + " " + (
                " && " if self.dictRule[obj["name"]].expression.index(j) < len(
                    self.dictRule[obj["name"]].expression) - 1 else " ")

        valueText += obj["name"] + " " + expr + " Then " + self.dictRule[obj["name"]].outputVar + " = " + self.dictRule[
            obj["name"]].value + '\n'
        return valueText

    def er(self):
        self.text = ft.TextField(value="Ошибка, исправтье БЗ", width=1000, multiline=True, disabled=True, text_size=10)
        self.column.controls = [self.text]
        self.update()

    def printAnswer(self, val):
        self.text = ft.TextField(value="", width=1000, multiline=True, disabled=True, text_size=10)
        self.LabelAnswer = ft.Text("Ответ:", size=30, weight=ft.FontWeight.BOLD)
        self.an = ft.Text(val.name + " : " + val.value if val.value != None else "Не удалось определить цель косультации", size=25)
        self.LabelRule = ft.Text("Порядок срабатывания правил:", size=30, weight=ft.FontWeight.BOLD)
        self.treeView = self.r(self.treeView)
        if len(self.treeView) > 0:
            self.print_val(self.treeView[0], self.treeView)
        else:
            self.text.value="Ни одно правило не сработало"
        text = "Рабочая память" + '\n'
        for i in self.varValue:
            text += i[0] + " = " + i[1] + '\n'


        self.Work = ft.TextField(value=text, width=1000, multiline=True, disabled=True, text_size=10)
        self.column.controls = [self.LabelAnswer, self.an, self.LabelRule, self.text, self.Work]

        data = logs.save_logs(self.file_name, self.text.value, self.Work.value)
        logs.save_logs_(data)

        self.update()

    def cretateQuestion(self, var):
        self.question.value = var.Question
        self.anserEnum.options = [ft.dropdown.Option(i) for i in self.dictDomain[var.Set].set]
        self.add.disabled = False
        self.update()

    def onButton(self, e):
        self.dictAnswer["Answer"] = self.anserEnum.value
        self.question.value=""
        self.anserEnum.value=""
        self.anserEnum.options = []
        self.add.disabled = True
        self.event.set()
        self.update()


    def reBuild(self, e):
        self.buttonStart.visible = False
        self.addBK = ft.ElevatedButton(text = "Выбрать БЗ", on_click=self.file_pickerLoad.pick_files(allow_multiple=False, allowed_extensions=["my_format"]))
        self.LabelQuestion = ft.Text("Вопрос", size=25)
        self.question = ft.TextField(value="", width=250, multiline=True, disabled=True)
        self.LabelAnswerOption = ft.Text("Вариант ответа", size=25)
        self.anserEnum = ft.Dropdown(options=[])
        self.add = ft.ElevatedButton(text="Ответить", width=250, on_click=self.onButton)
        self.column.controls.append(self.LabelQuestion)
        self.column.controls.append(self.question)
        self.column.controls.append(self.LabelAnswerOption)
        self.column.controls.append(self.anserEnum)
        self.column.controls.append(self.add)
        self.update()

    def build(self):
        self.file_pickerLoad = ft.FilePicker(on_result=self.OnLoadResult)
        self.buttonStart = ft.ElevatedButton(text = "Начать", on_click=self.reBuild)
        self.column = ft.Column(controls=[
            self.file_pickerLoad,
            self.buttonStart])
        return self.column

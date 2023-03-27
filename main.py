import flet as ft
import pickle

import domain
import variable
import rule

import varPage
import rulePage
import mainPage
import domainPage
import logPage


dictVar = {}
dictRule = {}
dictDomain = {}
listRule = {"listRule": []}
dictAnswer= {"Answer": "", "Var": ""}

#

def main(page: ft.Page):
    page.title = "ToDo App"

    def OnLoadResult(e: ft.FilePickerResultEvent):
        if e.files != None:
            with open(e.files[0].path, 'rb') as file:
                obj = pickle.load(file)

            for i in obj["dictDomain"]:
                dictDomain[i["name"]] = domain.Domain(i["name"], set(i["set"]))

            for i in obj["dictVar"]:
                dictVar[i["name"]] = variable.Variable(i["name"], i["type"], i["Set"], Question=i["Question"], Main=i["Main"])

            for i in obj["dictRule"]:
                l = []
                for j in i["expression"]:
                    l.append((j[0], j[1], j[2]))

                dictRule[i["name"]] = rule.Rule(i["name"], i["inputVar"], i["outputVar"], l, i["value"])

            listRule["listRule"] = obj["listRule"]


    def OnAddResult(e: ft.FilePickerResultEvent):

        dictRez = {"dictDomain": [], "dictVar":[], "dictRule": [], "listRule": []}

        for i in dictDomain:
            dictRez["dictDomain"].append(
                {
                    "name": i,
                    "set": list(dictDomain[i].set)
                }
            )

        for i in dictVar:
            dictRez["dictVar"].append(
                {
                    "name": i,
                    "type": dictVar[i].type,
                    "Question": dictVar[i].Question,
                    "Main": dictVar[i].Main,
                    "Set": dictVar[i].Set,
                }
            )

        for i in dictRule:
            l = []
            for j in dictRule[i].expression:
                l.append([j[0], j[1], j[2]])

            dictRez["dictRule"].append(
                {
                    "name": i,
                    "inputVar": dictRule[i].inputVar,
                    "outputVar": dictRule[i].outputVar,
                    "expression": l,
                    "value": dictRule[i].value
                }
            )
        dictRez["listRule"] = listRule["listRule"]

        with open(e.path+".my_format", 'wb') as outfile:
            pickle.dump(dictRez, outfile)


    file_pickerLoad = ft.FilePicker(on_result=OnLoadResult)
    file_pickerAdd = ft.FilePicker(on_result=OnAddResult)

    def onUseBase(e):
        dictDomain={}
        dictVar={}
        dictRule={}
        dictAnswer={}
        file_pickerLoad.pick_files(allow_multiple=False, allowed_extensions=["my_format"])
        page.go("/main")

    def route_change(route):
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                [
                    ft.AppBar(title=ft.Text("Главная"), bgcolor=ft.colors.SURFACE_VARIANT),
                    ft.Text(""),
                    ft.Row(controls=[
                        file_pickerLoad,
                        ft.ElevatedButton("Создать новую БЗ", on_click=lambda _: page.go("/main")),
                        ft.ElevatedButton("Использовать готовую", on_click=onUseBase),
                        ft.ElevatedButton("Пройти консультацию", on_click=lambda _:page.go("/consultation")),
                        ft.ElevatedButton("Просмотреть логи консультаций", on_click=lambda _:page.go("/logs"))
                    ])
                ],
                vertical_alignment=ft.MainAxisAlignment.START,
                scroll=ft.ScrollMode.AUTO,
            )
        )
        if page.route == "/rule":
            page.views.append(
                ft.View(
                    "/rule",
                    [
                        ft.AppBar(title=ft.Text("Правила"), bgcolor=ft.colors.SURFACE_VARIANT),
                        ft.Text("Перед переходом убедитесь что у вас нет не сохраненных полей", size=25),
                        ft.Row(controls=[
                            ft.ElevatedButton("Переменные", on_click=lambda _: page.go("/var")),
                            ft.ElevatedButton("Домены", on_click=lambda _: page.go("/domain"), width=300),
                            ft.ElevatedButton("Главная", on_click=lambda _: page.go("/main")),
                        ]),
                        rulePage.ListRule(dictVar, dictRule, listRule["listRule"], dictDomain),
                    ],
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.AUTO,
                )
            )

        if page.route == "/var":
            page.views.append(
                ft.View(
                    "/var",
                    [
                        ft.AppBar(title=ft.Text("Переменные"), bgcolor=ft.colors.SURFACE_VARIANT),
                        ft.Text("Перед переходом убедитесь что у вас нет не сохраненных полей. Что бы выбрать главную переменную нажминте на чекбокс.", size=25),
                        ft.Row(controls=[
                            ft.ElevatedButton("Правила", on_click=lambda _: page.go("/rule")),
                            ft.ElevatedButton("Домены", on_click=lambda _: page.go("/domain")),
                            ft.ElevatedButton("Главная", on_click=lambda _: page.go("/main")),
                        ]),
                        varPage.ListVar(dictVar, dictDomain, dictRule),
                    ],
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.AUTO,
                )
            )

        if page.route == "/main":
            page.views.append(
                ft.View(
                    "/main",
                    [
                        ft.AppBar(title=ft.Text("Редактирование БЗ"), bgcolor=ft.colors.SURFACE_VARIANT),
                        ft.Row(controls=[
                            file_pickerAdd,
                            ft.ElevatedButton("Перменные", on_click=lambda _: page.go("/var"), width=300),
                            ft.ElevatedButton("Правила", on_click=lambda _: page.go("/rule"), width=300),
                            ft.ElevatedButton("Домены", on_click=lambda _: page.go("/domain"), width=300),
                            ft.ElevatedButton("Сохранить",
                                              on_click=lambda _: file_pickerAdd.save_file(allowed_extensions=["my_format"]), width=300)
                        ],
                        alignment=ft.alignment.center,
                        )
                    ],
                    vertical_alignment = ft.MainAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.AUTO,
                )
            )

        if page.route == "/consultation":
            page.views.append(
                ft.View(
                    "/consultation",
                    [
                        ft.AppBar(title=ft.Text("Консультация"), bgcolor=ft.colors.SURFACE_VARIANT),
                        ft.Row(controls=[
                            mainPage.mainPage()
                        ])
                    ],
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.AUTO,
                )
            )


        if page.route == "/domain":
            page.views.append(
                ft.View(
                    "/domain",
                    [
                        ft.AppBar(title=ft.Text("Домены"), bgcolor=ft.colors.SURFACE_VARIANT),
                        ft.Text("Перед переходом убедитесь что у вас нет не сохраненных полей", size=25),
                        ft.Row(controls=[
                            ft.ElevatedButton("Правила", on_click=lambda _: page.go("/rule")),
                            ft.ElevatedButton("Перменные", on_click=lambda _: page.go("/var")),
                            ft.ElevatedButton("Главная", on_click=lambda _: page.go("/main")),
                        ]),
                        domainPage.ListDomain(dictDomain),
                    ],
                    vertical_alignment = ft.MainAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.AUTO,
                )
            )

        if page.route == "/logs":
            page.views.append(
                ft.View(
                    "/logs",
                    [
                        ft.AppBar(title=ft.Text("Результаты косультаций"), bgcolor=ft.colors.SURFACE_VARIANT),
                        ft.Row(controls=[
                            ft.ElevatedButton("Главная", on_click=lambda _: page.go("/")),
                        ]),
                        logPage.Logs(),
                    ],
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.AUTO,
                    )
            )

        page.scroll = "always"
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

ft.app(target=main)
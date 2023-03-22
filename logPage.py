import flet as ft
import logs

class Logs(ft.UserControl):
    def __init__(self):
        super(Logs, self).__init__()
        self.dict_logs = logs.load_logs()


    def on_change_files(self, e):
        file = self.files.value
        for i in self.dict_logs:
            if i["file_name"] == file:
                self.tree_view.value = i["value"]["tree_view"]
                self.Work.value = i["value"]["work_memory"]
                self.update()
                return


    def build(self):
        self.files = ft.Dropdown(options=[ft.dropdown.Option(i["file_name"]) for i in self.dict_logs], on_change=self.on_change_files)
        self.LabelRule = ft.Text("Порядок срабатывания правил:", size=30, weight=ft.FontWeight.BOLD)
        self.tree_view = ft.TextField(width=1000, multiline=True, disabled=True, text_size=10)
        self.LabelRule = ft.Text("Рабочая память:", size=30, weight=ft.FontWeight.BOLD)
        self.Work = ft.TextField(width=1000, multiline=True, disabled=True, text_size=10)
        return ft.Column(controls=[self.files, self.LabelRule, self.tree_view, self.LabelRule, self.Work])

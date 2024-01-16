import logging
import PySimpleGUI as sg
from inputs import CELL_MEDIUM, VALID_PROJECTS, VALID_BAC, VALID_UNITS, csv_input
import database_app as dapp
from outputs import to_word, to_word_bac,to_word_pr
from calc import bac_to_csv, cc_to_csv, pr_to_csv


log = logging.getLogger(__name__)

log = logging.getLogger(__name__)


class GUIApp:

    def __init__(self):
        self.in_files = []
        self.user_labels = []
        self.event_to_action = {
            "-CELL_LINE-": self.get_medium,

            "-DELETE_BAC-": self.delete_bac,
            "-DELETE_CC-": self.delete_cc,
            "-DELETE_PR-": self.delete_prot,

            "-ADD_BAC-": self.add_bac,
            "-ADD_CC-": self.add_cc,
            "-ADD_PR-": self.add_prot,

            "-EXPORT-": self.export,
            "-CLEAR-": self.clear,

            # tool bar menu
            "Bacteria": self.create_bac_window,
            "Cell line": self.create_cell_line_window,
            "Projects": self.create_project_window,
            "Units": self.create_unit_window


        }
        self.table_header_to_key = {
            "Název": "Název",

        }

    def __repr__(self):
        return {self}

    def __enter__(self):
        self.window = self.create_window()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.window.close()

    def __eat_events__(self):
        """Eats falsely fired events
        NOTE: https://github.com/PySimpleGUI/PySimpleGUI/issues/4268
        """
        while True:
            event, values = self.window.read(timeout=0)
            if event == '__TIMEOUT__':
                break
        return

    def run(self):
        while True:
            event, values = self.window.read()
            log.debug((event, values))

            if event == sg.WIN_CLOSED or event == "Close" or event == "Cancel":  # always,  always give a way out!
                break

            # do actions
            try:
                self.event_to_action[event](values)
                self.__eat_events__()


            except KeyError:
                log.exception('unknown event')
                print("unknown event")

    def create_window(self):
        sg.theme("Darkblue")
        def tool_bar_menu():
            menuBar_Layout = [
                ['&Edit', ['Bacteria', 'Cell line', 'Projects', 'Units']],
                ['&Help', ['&About...']]
            ]
            return menuBar_Layout

        def bac_tab():
            size = (25, 1)
            size2 = (15, 1)
            size3 = (10, 30)
            headrow = ["Assay", "Aliquotes", "Project", "Insert", "Bacteria", "Solution", "Conc", "date"]
            bac_layout = [
                [sg.Frame("Enter values", size=(412, 300), layout=[
                    [sg.Text("Assay no.: ", size=size), sg.InputText(key="-ASSAY_NO_BAC-", size=size2)],
                    [sg.Text("Amount of aligoutes: ", size=size),
                     sg.Input(key="-TOTAL_ALIQUOTES_BAC-", size=size2)],
                    [sg.Text("Solution: ", size=size), sg.Input(key="-SOL-", size=size2)],
                    [sg.Text("Project: ", size=size),
                     sg.OptionMenu(VALID_PROJECTS, key="-PROJECT_BAC-", size=size3)],
                    [sg.Text("Insert: ", size=size), sg.InputText(key="-INSERT-", size=size2)],
                    [sg.Text("Bacteria: ", size=size), sg.OptionMenu(VALID_BAC, key="-BAC-", size=size3)],
                    [sg.Text("concentration: ", size=size), sg.InputText(key="-CONC_BAC-", size=size2)],
                    [sg.Text("date: ", size=size), sg.InputText(key="-DATE_BAC-", size=size2),
                     sg.CalendarButton("chose", target="-DATE_BAC-", format="%d.%m.20%y", begin_at_sunday_plus=1,
                                       close_when_date_chosen=True, button_color=("Grey"))],
                    [sg.Text("")],
                    [sg.Push(), sg.Button("Add", button_color=("Grey"), key="-ADD_BAC-"),
                     sg.Button("Delete", button_color=("Grey"), key="-DELETE_BAC-"),
                     ]
                ]), sg.Frame("Entered values", size=(600, 300), layout=[
                    [sg.Table(values=[], headings=headrow, enable_events=True, pad=(0, 0), size=(600, 300), justification="centre", auto_size_columns=True, key="-LIST_BAC_TABLE-")]
                               ], key="-ENTERED_BAC-"),
                 ]
            ]
            return bac_layout

        def cc_tab():
            print("vytvoření okna")
            size = (25, 1)
            size2 = (15, 1)
            size3 = (10, 30)
            headrow = ["Assay", "Aliquotes", "Project", "Cell line", "Medium", "Conc", "date"]
            cc_layout = [
                         [sg.Frame("Enter values", size=(412, 300), layout=[
                             [sg.Text("Assay no.: ", size=size), sg.InputText(key="-ASSAY_NO_CC-", size=size2)],
                             [sg.Text("Amount of aligoutes: ", size=size),
                              sg.Input(key="-TOTAL_ALIQUOTES_CC-", size=size2)],
                             [sg.Text("Project: ", size=size),
                              sg.OptionMenu(VALID_PROJECTS, key="-PROJECT_CC-", size=size3)],
                             [sg.Text("Cell line: ", size=size),
                              sg.OptionMenu(CELL_MEDIUM.keys(), key="-CELL_LINE-", size=size3)],
                             [sg.Text("Medium: ", size=size),
                              sg.OptionMenu(CELL_MEDIUM.values(), key="-MEDIUM_CC-", size=size3)],
                             [sg.Text("concentration: [x10e6 cells/ml]", size=size),
                              sg.InputText(key="-CONC_CC-", size=size2)],
                             [sg.Text("date: ", size=size), sg.InputText(key="-DATE_CC-", size=size2),
                              sg.CalendarButton("chose", target="-DATE_CC-", format="%d.%m.20%y",
                                                begin_at_sunday_plus=1,
                                                close_when_date_chosen=True, button_color=("Grey"))],
                             [sg.Text("")],
                             [sg.Push(), sg.Button("Add", button_color=("Grey"), key="-ADD_CC-"),
                              sg.Button("Delete", button_color=("Grey"), key="-DELETE_CC-")]
                         ]), sg.Frame("Entered values", size=(600, 300), layout=[
                                   [sg.Table(values=[], headings=headrow, enable_events=True, pad=(0, 0), size=(600, 300), justification="centre", key="-LIST_CC_TABLE-")]
                               ]),
                          ]
                         ]
            return cc_layout

        def protein_tab():
            size = (25, 1)
            size2 = (15, 1)
            size3 = (10, 30)
            headrow = ["Alig", "Name", "Conc", "Unit", "Supplier", "Cat.No.", "Lot", "Date"]
            protein_layout = [
                              [sg.Frame("Enter values", size=(412, 300), layout=[
                                  [sg.Text("Amount of aligoutes: ", size=size), sg.Input(key="-TOTAL_ALIQUOTES_PR-", size=size2)],
                                  [sg.Text("Name: ", size=size), sg.InputText(key="-NAME_PR-", size=size2)],
                                  [sg.Text("Concentration:", size=size), sg.InputText(key="-CONC_PR-", size=size2)],
                                  [sg.Text("Unit", size=size), sg.OptionMenu(VALID_UNITS, key="-UNITS-", size=size3)],
                                  [sg.Text("Supplier", size=size), sg.InputText(key="-SUP-", size=size2)],
                                  [sg.Text("Cat. No.", size=size), sg.InputText(key="-CAT-", size=size2)],
                                  [sg.Text("Lot.", size=size), sg.InputText(key="-LOT-", size=size2)],
                                  [sg.Text("date: ", size=size), sg.InputText(key="-DATE_PR-", size=size2),
                                   sg.CalendarButton("chose", target="-DATE_PR-", format="%d.%m.20%y",
                                                     begin_at_sunday_plus=1,
                                                     close_when_date_chosen=True, button_color=("Grey"))],
                                  [sg.Text("")],
                                  [sg.Push(), sg.Button("Add", button_color=("Grey"), key="-ADD_PR-"),
                                   sg.Button("Delete", button_color=("Grey"), key="-DELETE_PR-"), ]
                              ]),
                               sg.Frame("Entered values", size=(600, 300), layout=[
                                   [sg.Table(values=[], headings=headrow, enable_events=True, pad=(0, 0), size=(600, 300), justification="centre", key="-LIST_PR_TABLE-")]
                               ])
                               ]
                              ]
            return protein_layout

        layout = [[sg.Menu(tool_bar_menu())],
                  [sg.TabGroup([[sg.Tab("Bacterial", layout=bac_tab(), key="-BAC_TAB-"),
                                 sg.Tab("Cell Culture", layout=cc_tab(), key="-CC_TAB-"),
                                 sg.Tab("Protein", layout=protein_tab(), key="-PR_TAB-")]]
                               )],
                  [sg.Push(), sg.Button("Clear", key="-CLEAR-"), sg.Button("Export", key="-EXPORT-"), sg.Button("Close")]
                  ]

        window = sg.Window("Label maker", layout, auto_size_text=True, finalize=True)
        return window


    # okna, která se otevřou z toolbar menu
    def create_bac_window(self, values):
        print("creating bacteria window :-)")

        def add_new_bac_window():
            print("jsem v add_new_bac_window")
            b_layout = [[sg.Text("Bacteria: "), sg.InputText(key="-ADDING_BACTERIA-")],
                        [sg.Text("")],
                        [sg.Push(), sg.Button("Add", key="-ADD_NEW_BAC-"), sg.Button("Cancel", key="-CANCEL-")]
                        ]
            b_window = sg.Window("Add new bacteria", b_layout, finalize=True)
            while True:
                ev, val = b_window.read()
                if ev == "-CANCEL-" or ev == sg.WIN_CLOSED:
                    break
                elif ev == "-ADD_NEW_BAC-":
                    item = (val["-ADDING_BACTERIA-"])
                    if item == "":
                        sg.popup_ok("Warning \nYou did not add any text")
                    else:
                        dapp.add_bac(item)
                        print("New bacteria added", item)
                b_window.close()
        def change_bac():
            print("Jsem ve změnit")

        dapp.bac_database_con()
        sg.theme("DarkBlue")
        layout = [
            [sg.Text("Bacteria ")],
            [sg.Listbox(values=[], key="-ZAZ-", size=(50, 20), select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE)],
            [sg.Push(), sg.Button("New bacteria", key="-ADD_B-"),  sg.Button("Change", key='-CHANGE-'),
             sg.Button("Delete bacteria", key="-DELETE_BAC-"), sg.Button("Cancel", key="Close")]]
        window = sg.Window("Bacteria", layout, auto_size_text=True, finalize=True)
        window["-ZAZ-"].Update(dapp.bac_database_con())
        while True:
            window["-ZAZ-"].Update(dapp.bac_database_con())
            event, values = window.read()
            if event == "Close" or event == sg.WIN_CLOSED:
                break
            elif event == "-ADD_B-":
                print("Opening bacteria adding window")
                add_new_bac_window()
            elif event == "-CHANGE-":
                chosen = window["-ZAZ-"].get()
                print(chosen)
                print("změněno")
            elif event == "-DELETE_BAC-":
                chosen = window["-ZAZ-"].get()
                layout = [[sg.Text("Do you really want delete?", justification="c")],
                          [sg.Text(chosen, justification="c")],
                          [sg.Push(), sg.Button("yes"), sg.Button("no"), sg.Push()]
                          ]
                window_yn = sg.Window(f"Yes/No", layout, finalize=True)
                while True:
                    event, values = window_yn.read()
                    if event == sg.WIN_CLOSED or event == "no":
                        break
                    elif event == "yes":
                        print("yes was chosen")
                        for index, value in enumerate(chosen):
                            first_item = value[0]
                            no = first_item
                            print(no)
                            dapp.delete_bac(no)
                        print("done", chosen)
                        window_yn.close()
        window.close()

    def create_cell_line_window(self, values):
        print("creating cell culture window")

        def add_cell_line():
            layout = [[sg.Text("cell line: "), sg.InputText(key="-ADDING_CELL_LINE-")],
                      [sg.Text("medium: "), sg.InputText(key="-ADDING_CC_MEDIUM-")],
                      [sg.Text("")],
                      [sg.Push(), sg.Button("Add", key="-ADD_CELL_LINE-"), sg.Button("Cancel", key="-C-")]
                      ]

            cc_window = sg.Window("Add cell line", layout, auto_size_text=True, finalize=True)
            while True:
                cc_event, cc_values = cc_window.read()
                if cc_event == "-C-" or cc_event == sg.WIN_CLOSED:
                    break
                elif cc_event == "-ADD_CELL_LINE-":
                    item = (cc_values["-ADDING_CELL_LINE-"], cc_values["-ADDING_CC_MEDIUM-"])
                    if item == ("", ""):
                        sg.popup_ok("Warning", "You did not add any text")
                    else:
                        window["-ZAZ-"].Update(dapp.add_cell_culture(item))
                        dapp.add_cell_culture(item)
                        print("New culture added", item)
                    cc_window.close()

        dapp.cell_culture_database_con()

        layout = [[sg.Text("cell line"), sg.Text("medium")],
                  [sg.Listbox(values=[], key="-ZAZ-", size=(50, 20), select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE)],
                  [sg.Push(), sg.Button("New line", key="-ADD_LINE-"), sg.Button("Delete line", key="-DELETE_LINE-"),
                   sg.Button("Cancel", key="Close")]]
        window = sg.Window("Cell lines", layout, auto_size_text=True, finalize=True)
        while True:
            window["-ZAZ-"].Update(dapp.cell_culture_database_con())
            event, values = window.read()
            if event == "Close" or event == sg.WIN_CLOSED:
                break
            elif event == "-ADD_LINE-":
                print("opening adding window")
                add_cell_line()
            elif event == "-DELETE_LINE-":
                chosen = window["-ZAZ-"].get()
                layout = [[sg.Text("Do you really want delete?", justification="c")],
                          [sg.Text(chosen, justification="c")],
                          [sg.Push(), sg.Button("yes"), sg.Button("no"), sg.Push()]
                          ]
                window_yn = sg.Window(f"Yes/No", layout, finalize=True)
                while True:
                    event, values = window_yn.read()
                    if event == sg.WIN_CLOSED or event == "no":
                        break
                    elif event == "yes":
                        print("yes was chosen")
                        for index, value in enumerate(chosen):
                            first_item = value[0]
                            no = first_item
                            print("first item: ", no)
                            dapp.delete_cell_culture(no)
                        print("done", chosen)
                        window_yn.close()
        window.close()

    def create_project_window(self, values):
        print("creating project window")

        def add_new_project_window():
            add_project_layout = [
                [sg.Text("No: "), sg.InputText(key="-ADDING_NO-")],
                [sg.Text("Name: "), sg.InputText(key="-ADDING_NAME-")],
                [sg.Text("Status: "), sg.InputText(key="-ADDING_STATUS-")],
                [sg.Text("")],
                [sg.Push(), sg.Button("Add", key="-PROJECT_ADD-"), sg.Button("Cancel", key="-CANCEL-")]]
            add_project_window = sg.Window("Add new project", add_project_layout, finalize=True)
            while True:
                pr_event, val = add_project_window.read()
                if pr_event == "-CANCEL-" or event == sg.WIN_CLOSED:
                    break
                if pr_event == "-PROJECT_ADD-":
                    item = (val["-ADDING_NO-"], val["-ADDING_NAME-"], val["-ADDING_STATUS-"])
                    if item == ("", "", ""):
                        sg.popup_ok("Warning", "Any text was entered")
                    else:
                        dapp.add_project(item)
                        print("New project added", item)

            add_project_window.close()

        dapp.project_database_con()

        sg.theme("DarkBlue")
        layout = [
            [sg.Text("No "), sg.Text("Name "), sg.Text("Status ")],
            [sg.Listbox(values=[], key="-ZAZ-", size=(50, 20), select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE)],
            [sg.Push(), sg.Button("New project", key="-ADD_PROJECT-"),
             sg.Button("Delete project", key="-DELETE_PROJECT-"), sg.Button("Cancel", key="Close")]]
        window = sg.Window("Projects", layout, auto_size_text=True, finalize=True)
        window["-ZAZ-"].Update(dapp.project_database_con())
        while True:
            window["-ZAZ-"].Update(dapp.project_database_con())
            event, values = window.read()
            if event == "Close" or event == sg.WIN_CLOSED:
                break
            elif event == "-ADD_PROJECT-":
                print("Opening project adding window")
                add_new_project_window()
            elif event == "-DELETE_PROJECT-":
                chosen = window["-ZAZ-"].get()
                layout = [[sg.Text("Do you really want delete?", justification="c")],
                          [sg.Text(chosen, justification="c")],
                          [sg.Push(), sg.Button("yes"), sg.Button("no"), sg.Push()]
                          ]
                window_yn = sg.Window(f"Yes/No", layout, finalize=True)
                while True:
                    event, values = window_yn.read()
                    if event == sg.WIN_CLOSED or event == "no":
                        break
                    elif event == "yes":
                        print("yes was chosen")
                        for index, value in enumerate(chosen):
                            first_item = value[0]
                            no = first_item
                            print(no)
                            dapp.delete_project(no)
                        print("done", chosen)
                        window_yn.close()
        window.close()

    def create_unit_window(self, values):
        print("creating unit window :-)")

        def add_new_unit_window():
            print("jsem v add_new_unit_window")
            b_layout = [[sg.Text("unit: "), sg.InputText(key="-ADDING_UNIT-")],
                        [sg.Text("")],
                        [sg.Push(), sg.Button("Add", key="-ADD_NEW_UNIT-"), sg.Button("Cancel", key="-CANCEL-")]
                        ]
            u_window = sg.Window("Add new unit", b_layout, finalize=True)
            while True:
                ev, val = u_window.read()
                if ev == "-CANCEL-" or ev == sg.WIN_CLOSED:
                    break
                elif ev == "-ADD_NEW_UNIT-":
                    item = (val["-ADDING_UNIT-"])
                    if item == "":
                        sg.popup_ok("Warning \nYou did not add any text")
                    else:
                        dapp.add_unit(item)
                        print("New unit added", item)
                u_window.close()

        dapp.protein_database_con()
        sg.theme("DarkBlue")
        layout = [
            [sg.Text("Units ")],
            [sg.Listbox(values=[], key="-ZAZ-", size=(50, 20), select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE)],
            [sg.Push(), sg.Button("New unit", key="-ADD_U-"),
             sg.Button("Delete unit", key="-DELETE_U-"), sg.Button("Cancel", key="Close")]]
        window = sg.Window("Units", layout, auto_size_text=True, finalize=True)
        window["-ZAZ-"].Update(dapp.protein_database_con())
        while True:
            window["-ZAZ-"].Update(dapp.protein_database_con())
            event, values = window.read()
            if event == "Close" or event == sg.WIN_CLOSED:
                break
            elif event == "-ADD_U-":
                print("Opening units adding window")
                add_new_unit_window()
            elif event == "-DELETE_U-":
                chosen = window["-ZAZ-"].get()
                layout = [[sg.Text("Do you really want delete?", justification="c")],
                          [sg.Text(chosen, justification="c")],
                          [sg.Push(), sg.Button("yes"), sg.Button("no"), sg.Push()]
                          ]
                window_yn = sg.Window(f"Yes/No", layout, finalize=True)
                while True:
                    event, values = window_yn.read()
                    if event == sg.WIN_CLOSED or event == "no":
                        break
                    elif event == "yes":
                        print("yes was chosen")
                        for index, value in enumerate(chosen):
                            first_item = value[0]
                            no = first_item
                            print(no)
                            dapp.delete_unit(no)
                        print("done", chosen)
                        window_yn.close()
        window.close()

    # jiné funkce
    def get_medium(self, values):
        # přiřadí správné médim k buněčné linii podle vstupního slovníku CELL_MEDIUM
        print("přiřazení média")
        medium = CELL_MEDIUM.get(values["-C-"])
        return medium

    def clear(self, values):  # smaže hodnoty v "Entered values" části okna
        # TODO: zajistit, aby se vymazalo jen data v otevřené záložce

        bac_table = self.window["-LIST_BAC_TABLE-"]
        cc_table = self.window["-LIST_CC_TABLE-"]
        pr_table = self.window["-LIST_PR_TABLE-"]
        if bac_table != "":
            #self.window["-BAC_TAB-"].select()
            self.window["-LIST_BAC_TABLE-"].Update("")
            print("Bac - okno Entered values vyčištěno")
        if cc_table != "":
            self.window["-LIST_CC_TABLE-"].Update("")
            print("CC - okno 'Entered values' vymazáno")
        if pr_table != "":
            self.window["-LIST_PR_TABLE-"].Update("")
            print("Prot - okno 'Entered values' vymazáno")

    # mazací funkce - vymaže zadané hodnoty v "Enter values" části okna
    def delete_bac(self, values):
        print("zadané hodnoty smazány")
        self.window["-ASSAY_NO_BAC-"].Update("")
        self.window["-SOL-"].Update("")
        self.window["-TOTAL_ALIQUOTES_BAC-"].Update("")
        self.window["-PROJECT_BAC-"].Update("")
        self.window["-INSERT-"].Update("")
        self.window["-BAC-"].Update("")
        self.window["-CONC_BAC-"].Update("")
        self.window["-DATE_BAC-"].Update("")

    def delete_cc(self, values):
        self.window["-ASSAY_NO_CC-"].Update("")
        self.window["-TOTAL_ALIQUOTES_CC-"].Update("")
        self.window["-PROJECT_CC-"].Update("")
        self.window["-CELL_LINE-"].Update("")
        self.window["-MEDIUM_CC-"].Update("")
        self.window["-CONC_CC-"].Update("")
        self.window["-DATE_CC-"].Update("")

    def delete_prot(self, values):
        self.window["-NAME_PR-"].Update("")
        self.window["-CONC_PR-"].Update("")
        self.window["-UNITS-"].Update("")
        self.window["-SUP-"].Update("")
        self.window["-CAT-"].Update("")
        self.window["-LOT-"].Update("")
        self.window["-DATE_PR-"].Update("")

    # přidávací funkce - přidájí zadané hodnoty do "Entered vaues" části okna
    def add_bac(self, values):
        print("zadané hodnoty byly přídány")
        try:
            assay = str(values["-ASSAY_NO_BAC-"])
            solution = str(values["-SOL-"])
            project = str(values["-PROJECT_BAC-"])
            insert = str(values["-INSERT-"])
            bacteria = str(values["-BAC-"])

            total_aliquotes = int(values["-TOTAL_ALIQUOTES_BAC-"])
            batch_no = 0
            data = []
            for cislo in range(total_aliquotes):
                batch_no += 1
                assay = str(values["-ASSAY_NO_BAC-"])
                aliq = f'{batch_no}/{values["-TOTAL_ALIQUOTES_BAC-"]}'
                project = (values["-PROJECT_BAC-"])
                insert = (values["-INSERT-"])
                bacteria = (values["-BAC-"])
                solution = (values["-SOL-"])
                conc = int(values["-CONC_BAC-"])
                conc_str = str(conc)
                date = str(values["-DATE_BAC-"])
                data.append([assay, aliq, project, bacteria, solution, conc_str, date])
                self.window["-LIST_BAC_TABLE-"].update(data)

            if assay == "" or solution == "" or project == ("", "") or insert == "" or bacteria == "" or date == "":
                print("žádné pole nesmí být prázdné")
                sg.PopupOK("Missing values")
        except ValueError:
            print("špatně zadaná hodnota")
            sg.PopupOK("Inccorectly added number")

    def add_cc(self, values):
        try:
            assay = str(values["-ASSAY_NO_CC-"])
            project = str(values["-PROJECT_CC-"])
            cell = str(values["-CELL_LINE-"])
            medium = str(values["-MEDIUM_CC-"])

            total_aliquotes = int(values["-TOTAL_ALIQUOTES_CC-"])
            batch_no = 0
            data = []
            for cislo in range(total_aliquotes):
                batch_no += 1
                assay = str(values["-ASSAY_NO_CC-"])
                aliq = f'{batch_no}/{values["-TOTAL_ALIQUOTES_CC-"]}'
                project = (values["-PROJECT_CC-"])
                cells = (values["-CELL_LINE-"])
                medium = (values["-MEDIUM_CC-"])
                conc = int(values["-CONC_CC-"])
                conc_str = str(conc)
                date = str(values["-DATE_CC-"])
                data.append([assay, aliq, project, cells, medium, conc_str, date])
                self.window["-LIST_CC_TABLE-"].update(data)
            if assay == "" or project == ("", "") or cell == "" or medium == "" or conc == "" or date == "":
                print("žádné pole nesmí být prázdné")
                sg.PopupOK("Missing values")
        except ValueError:
            print("špatně zadaná hodnota")
            sg.PopupOK("Inccorectly added number")

    def add_prot(self, values):
        try:
            name = str(values["-NAME_PR-"])
            unit = str(values["-UNITS-"])
            supplier = str(values["-SUP-"])
            cat_no = str(values["-CAT-"])
            lot = str(values["-LOT-"])

            total_aliquotes = int(values["-TOTAL_ALIQUOTES_PR-"])
            batch_no = 0
            data = []
            for cislo in range(total_aliquotes):
                batch_no += 1
                aliq = f'{batch_no}/{values["-TOTAL_ALIQUOTES_PR-"]}'
                name = str(values["-NAME_PR-"])
                conc = int(values["-CONC_PR-"])
                conc_str = str(conc)
                unit = str(values["-UNITS-"])
                supplier = str(values["-SUP-"])
                cat_no = str(values["-CAT-"])
                lot = str(values["-LOT-"])
                date = str(values["-DATE_PR-"])
                data.append([aliq, name, conc_str, unit, supplier, cat_no, lot, date])
                self.window["-LIST_PR_TABLE-"].update(data)

            if name == "" or unit == ("") or supplier == "" or cat_no == "" or lot == "":
                print("žádné pole nesmí být prázdné")
                sg.PopupOK("Missing values")
        except ValueError:
            print("špatně zadaná hodnota")
            sg.PopupOK("Inccorectly added number")

    # tlačítkové funkce
    def export(self, values):
        try:
            # bac tab
            bac = vars(self.window["-LIST_BAC_TABLE-"])
            bac = bac["Values"]
            klice = ["assay", "aliquotes", "project", "insert", "bacteria", "solution", "conc", "date"]
            bac_to_csv(klice, bac)
            bac_data = csv_input("templates/bac_data.csv") #("templates/sample_data_bac.csv")
            to_word_bac(bac_data, "templates/template.docx")

            # cell line tab
            cc = vars(self.window["-LIST_CC_TABLE-"])
            cc = cc["Values"]
            klice = ["assay_no","aliquotes","project","cell_line","medium","conc","date"]
            cc_to_csv(klice, cc)
            cc_data = csv_input("templates/cc_data.csv")  #('templates/sample_data.csv')
            to_word(cc_data, 'templates/template.docx')

            # protein tab
            pr = vars(self.window["-LIST_PR_TABLE-"])
            pr = pr["Values"]
            klice = ["aliquotes","name","conc","unit","supplier","c","lot","date"]
            pr_to_csv(klice, pr)
            pr_data = csv_input("templates/pr_data.csv") #("templates/sample_data_pr.csv")
            to_word_pr(pr_data, "templates/template.docx")
            print("exportuji: ", bac, cc, pr)
        except IndexError:
            print("něco je prázdné")


        #sg.theme("DarkBlue")
        #MAX_ROWS = 12
        #MAX_COL = 5
        #layout = [[sg.Text("Chose where print starts", justification="centre", )],
         #         [sg.Text("", size=(1, 1))],
          #        [[sg.Button('', size=(5, 1), button_color=("white", "LightGrey"), key=(i, j), pad=(0, 0)) for j in range(MAX_COL)] for i in range(MAX_ROWS)],
           #       [sg.Text("", size=(1, 1))],
            #      [sg.Push(), sg.Button("OK"), sg.Button("Cancel"), sg.Push()]]
        #window_print = sg.Window("", layout=layout, finalize=True)
        #while True:
         #   print_event, values = window_print.read()
          #  if print_event == sg.WIN_CLOSED or print_event == "Cancel":
           #     break
            #elif print_event == "OK":
                #data =
                #to_word(data,'templates/template.docx')
             #   print("vytiskne se to od vybraného pole")
            #window_print[print_event].update(button_color=('white', 'DarkBlue'))
        #window_print.close()



def gui_main():
    log.info('starting gui app')

    with GUIApp() as gui:
        gui.run()

    return 0

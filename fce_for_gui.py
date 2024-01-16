import PySimpleGUI as sg

sg.theme("DarkBlue")
headrow = ["No.","Aliguotes","Name", "Status",]
rows = [["01", "internal", "ongoing"], ["02", "TIM3", "done"]]


layout = [[sg.Frame("Enter values",layout=[[sg.Text("no."), sg.Input(key="-NO-")],
          [sg.Text("Name"), sg.Input(key="-NAME-")],
          [sg.Text("Status"), sg.Input(key="-STATUS-")], [sg.Text("Aliq"), sg.Input(key="-Al-")]]),
           sg.Frame("Entered values", layout=[[sg.Table(values=rows, headings=headrow, auto_size_columns=True, justification="center",
                                                        select_mode=sg.TABLE_SELECT_MODE_EXTENDED, enable_events=True, key="-TABLE-")]])],
          [sg.Push, sg.Button("OK"), sg.Button("DEL"), sg.Button("Close")]]

window = sg.Window("okno", layout=layout, finalize=True)

while True:
    event, values = window.read()
    if event == "Close" or event == sg.WIN_CLOSED:
        break
    elif event == "OK":
        no = str(values["-NO-"])
        aliq = int(values["-Al-"])
        name = str(values["-NAME-"])
        status = str(values["-STATUS-"])
        window["-TABLE-"].update([[no, aliq,name, status]])
        print(no, name, status)
    elif event == "DEL":
        chosen = window["-TABLE-"].get()
        print(chosen)

window.close()

# (values=rows, headings=toprow, auto_size_columns=True, display_row_numbers=False, justification='center', key='-TABLE-', selected_row_colors='red on yellow',
#  enable_events=True, expand_x=True, expand_y=True, enable_click_events=True)
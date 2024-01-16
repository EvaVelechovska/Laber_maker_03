import PySimpleGUI as sg

sg.theme("DarkBlue")
MAX_ROWS = 12
MAX_COL = 5
layout = [[sg.Text("Chose where print starts", justification="centre", )],
          [sg.Text("", size=(1, 1))],
          [[sg.Button('', size=(5, 1), button_color=("white", "LightGrey"), key=(i, j), pad=(0, 0)) for j in
            range(MAX_COL)] for i in range(MAX_ROWS)],
          [sg.Text("", size=(1, 1))],
          [sg.Push(), sg.Button("OK"), sg.Button("Cancel"), sg.Push()]]
window_print = sg.Window("", layout=layout, finalize=True)
while True:
    print_event, values = window_print.read()
    if print_event == sg.WIN_CLOSED or print_event == "Cancel":
        break
    elif print_event == "OK":
        # data =
        # to_word(data,'templates/template.docx')
        print("vytiskne se to od vybraného pole")
    window_print[print_event].update(button_color=('white', 'DarkBlue'))
window_print.close()
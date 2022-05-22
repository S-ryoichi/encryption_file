import PySimpleGUI as sg
import subprocess as sp
import requests

password = "password"
OUT_PATH = "/mnt/c/Users/ryoichi/Desktop/hoge/"
URL = "http://example.com"

def setup():
    sg.theme('Dark Brown6')

    layout = [[sg.Text("File upload console")],
              [sg.Button("Choose File", key="choose_file")],
              [sg.MLine(key="file_list"+sg.WRITE_ONLY_KEY, size=(50,10)), sg.Button("Send", key="send")],
              [sg.Button("Exit")],
    ]

    window = sg.Window('Theme Browser', layout)
    return window

def choose_file():
    file = []
    value = sg.popup_get_file('get file multi', multiple_files=True)
    filename = value.split(";")
    return filename

def main(window):
    while True:
        event, values = window.read()
        # Exit the application when the "Exit" button pushed
        if event in (sg.WIN_CLOSED, "Exit"):
            return 0
        elif event == "choose_file":
            filelist = choose_file()
            window['file_list'+sg.WRITE_ONLY_KEY].print("\n".join(filelist))
        elif event == "send":
            for file in filelist:
                filename = file.split("/")[-1]
                sp.run(["openssl", "enc", "-aes-256-ctr", "-e", "-kfile", "key.txt", "-k", password, "-in", file, "-out", OUT_PATH + filename, "-base64"])
                sendfile = {"uploadFile": open(OUT_PATH + filename, "rb")}
                response = requests.post(url, files=sendfile)
            sg.popup("These files has sent.", title="Notion")
            return 0


if __name__ == "__main__":
    window = setup()
    main(window)
    window.close()
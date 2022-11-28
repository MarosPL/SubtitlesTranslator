# pip install googletrans==3.1.0a0
# pip install tkinter

import googletrans
import tkinter
import tkinter.messagebox
from tkinter import *
from tkinter import filedialog


def Main():
    src_lng = 'en'
    dest_lng = 'pl'
    src_path = GetInputFile()
    if src_path == '':
        exit()
    dest_path = src_path[:str.rindex(src_path, '.')] + '_pl.srt'

    print("Script is running...")

    TranslateFile(src_path, dest_path, src_lng, dest_lng)

    print("Script completed the task successfuly!")
    print("Translated file: " + dest_path)


def TranslateFile(src_path, dest_path, src_lng, dest_lng):
    translator = googletrans.Translator()

    # open source file
    subtitle_file_eng = open(src_path, 'r', encoding='utf=8')
    text_string = subtitle_file_eng.readlines()

    # loop through all lines
    output = ''
    try:
        for index, line in enumerate(text_string):
            line = line.strip()
            if line.strip("\n") and not line.isnumeric() and not line.startswith('00'):
                nextrow = text_string[index + 1]
                previousrow = text_string[index - 1]
                if not nextrow == '\n' and previousrow.startswith('00'):
                    translation = translator.translate(
                        line + ' ' + text_string[index + 1], src=src_lng, dest=dest_lng)
                    output += translation.text + "\n"
                elif nextrow == '\n' and not previousrow.startswith('00'):
                    continue
                else:
                    translation = translator.translate(
                        line, src=src_lng, dest=dest_lng)
                    output += translation.text + "\n"
            else:
                output += line + "\n"
    except IndexError:
        pass

    # save destination file
    subtitle_file_pl = open(dest_path, 'w', encoding='utf=8')
    subtitle_file_pl.writelines(output)
    subtitle_file_pl.close()


def GetInputFile():
    response = False
    while response == False:
        root = Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        root.filename = filedialog.askopenfilename(
            initialdir="/", title="Select subtitles file", filetypes=[("SRT", "*.srt"), ("ALL", '*.*')])
        if not root.filename:
            response = tkinter.messagebox.askyesno(
                "No file selected", "Do you want to quit?")
            if response:
                break
        else:
            response = True
    return root.filename


Main()

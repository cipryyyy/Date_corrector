from tqdm import tqdm
from tkinter import filedialog
import time
import os
import datetime
import exifread
from win32_setctime import setctime
import traceback
import sys
import os

def change_meta(path, new_value):
    setctime(path, datetime.datetime.timestamp(new_value))

def getData(path):                  #get EXIF file data
    with open(path, 'rb') as fh:
        tags = exifread.process_file(fh, stop_tag = "EXIF DateTimeOriginal")
        dateTaken = tags["EXIF DateTimeOriginal"]
        return datetime.datetime.strptime(str(dateTaken), '%Y:%m:%d %H:%M:%S')

def initialize():   #File explorer
    print("SSelect the folder with all your files")
    time.sleep(2)
    root = filedialog.askdirectory()
    return root

def counter(folder):    #count file in fodler
    return len(os.listdir(folder)), os.listdir(folder)

def gridize(strings, column, sep, downline = False):          #TUIG
    output = ""       #blank
    sep=sep + "  "
    
    for string in strings:
        if len(string) > column:
            output += ("..." + string[-(column-3):])        #name is too long
            output += "  "
        else:
            spaces = column-len(string)
            output += string
            for _ in range(spaces+2):
                output += " "
        output += sep

    if downline==True:              #like header
        output += "\n"
        for _ in range(column*len(strings)+len(strings)*len(sep)+2*(len(strings)-1)):       #nerdy things
            output += "-"
    return output

if __name__ == "__main__":
    title=False
    wide = 40         #column width
    work = ""
    
    try:
        folder = initialize()
        print(f"Folder: {folder}")
        process_len, files = counter(folder)
        print(f"Number of files: {process_len}")

        for i in tqdm(range(process_len), "Editing", unit = "media"):
            file = os.path.join(folder, files[i])
            work = file
            
            if title == False:
                tqdm.write(gridize(["FILE", "Creation date:", "Changed in:"], wide, "||", downline = True))
                title = True
            
            if file.split(".")[-1] == "jpg":            #jpg file check
                taken = getData(file)
                tqdm.write(gridize([f"{file}", f"{datetime.datetime.fromtimestamp(os.stat(file).st_ctime)}", f"{taken} [{int(datetime.datetime.timestamp(taken))}]"], wide, "||"))
                change_meta(file, taken)        #call
            else:
                tqdm.write(f"{file} ignored")
        input("Press ENTER...")

    except Exception:
        print(f"ERROR\ntraceback saved in {os.path.join(sys.path[0], 'log.txt')}")        #log file ts
        
        #traceback
        exc_info=sys.exc_info()
        err=traceback.format_exception(*exc_info)
        err.append(work)
        
        with open(os.path.join(sys.path[0], "log.txt"), "w") as f:
            for line in err:
                f.write(line)
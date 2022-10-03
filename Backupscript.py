import shutil
from datetime import date
import os
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
import time

# Get today's date
today = date.today()
today_format = today.strftime("%d_%b_%Y_")

# Source files/directories and destination
source_list = ["E:\\Backuptest\\angiking.jpg", "E:\\testing", "E:\\Battlescribe"]
drive_destination = "E:\\Backups"
g_login = GoogleAuth()
g_login.LocalWebserverAuth()
drive = GoogleDrive(g_login)
id = "1wj37ev8RM2lmEj-tXvnwbhSS-gj99ZZc"

def save_to_google_drive(combinedName, files):
    #if path is a directory, zip the directory and upload it
    if os.path.isdir(files):
        archiv = shutil.make_archive(combinedName, "gztar", files)
        gfile = drive.CreateFile({'title': combinedName + ".zip", 'parents': [{'id': id}]})
        gfile.SetContentFile(archiv)
        upload(combinedName, gfile, archiv)

    #if path is a file, zip the directory and upload it
    if os.path.isfile(files):
        gfile = drive.CreateFile({'title': combinedName, 'parents': [{'id': id}]})
        gfile.SetContentFile(files)
        upload(combinedName, gfile, files)


def upload(combinedName, gfile, uploaded_file):
    gfile.SetContentFile(uploaded_file)
    try:
        print(f"Uploading {combinedName}...")
        gfile.Upload()
        print(f"Upload complete\n")
    except:
        print("Connection error. Retrying..")
        time.sleep(2)
        upload(combinedName, gfile, uploaded_file)

def clear_zips(combinedName):
    os.remove(combinedName + ".tar.gz")

def save_to_disk(fileSplit, combinedName, files):
    newDest = drive_destination + "\\" + fileSplit
    # Check if folder exists for this file, if not, make one
    if fileSplit not in os.listdir(drive_destination):
        os.mkdir(drive_destination + "\\" + fileSplit)
    # if the folder for this file exists, copy file into the folder
    for folder in os.listdir(drive_destination):
        # if the source is a directory, copy entire directory
        if os.path.isdir(files):
            shutil.copytree(files, newDest + "\\" + combinedName, dirs_exist_ok=True)
        else:
            shutil.copy2(files, os.path.join(newDest + "\\" + combinedName))


def file_parsing(today_format, source_list, drive_destination):
    for files in source_list:
        fileSplit = files.split("\\")[-1]
        combinedName = today_format + fileSplit
        save_to_disk(fileSplit, combinedName, files)
        save_to_google_drive(combinedName, files)
        # if os.path.isdir(files):
        #     clear_zips(combinedName)
file_parsing(today_format, source_list, drive_destination)
time.sleep(5)
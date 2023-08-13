
import os
import glob
import shutil
import win32api

def get_external_drive_letter(name):
    print("Available drives: ")

    drives = win32api.GetLogicalDriveStrings()
    drives = drives.split("\000")[:-1]
    for drive in drives:
        if os.path.exists(drive):
            print(drive)
            volume_name = win32api.GetVolumeInformation(drive)[0]
            if volume_name == name:
                print(str(name) + " found on drive: " + str(drive))
                return drive
    return None

def copyToF(target_dir):
    # Get the current directory
    current_dir = os.getcwd()
    # Collect all files in the current directory into a list object
    file_list = [f for f in glob.glob(current_dir + "/*") if os.path.isfile(f)]

    # Deposit the files from the list into the target directory
    for file in file_list:
        file_name = os.path.basename(file)
        target_file = os.path.join(target_dir, file_name)
        shutil.copy(file, target_file)

    print(os.path.basename(target_dir))

    return len(file_list)

if __name__ == '__main__':

    drive_nickname = "PYBFLASH"
    target_dir = get_external_drive_letter(drive_nickname)

    if target_dir != None:
        print("Attempting to transfer contents of " + str(os.getcwd()) + " to " + str(target_dir) + "...")
        count = copyToF(target_dir)
        print(str(count) + " files successfully copied")

    else:
        print("Could not find drive " + drive_nickname)

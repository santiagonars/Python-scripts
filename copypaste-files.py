#PURPOSE: this script copies and pastes files form one directory to another
#**********************************************************************************
import os
import shutil

def main():
    #source path -> In command line, type 'pwd' while in directory location
    src = '/Users/santiagonorena/Downloads/pytorch-hackaton-downloads' 
    #destination path
    dest = '/Users/santiagonorena/Desktop/pytorch-hackaton'
    #use os.listdir() to get the files in the source and destination directory
    src_files = os.listdir(src)
    dest_files = os.listdir(dest)
    for filename in src_files: 
        full_filename = os.path.join(src, filename)
        #os.path.isfile() to see if they are regular files
        #statement does not copy files that are already in destination
        if (os.path.isfile(full_filename)) and (filename != "copyfiles.py") and (filename not in dest_files):
            #Copy a file with new name
            shutil.copy(full_filename, dest)
            print(filename)


if __name__ == '__main__':
    main()
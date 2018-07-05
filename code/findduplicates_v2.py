"""Find duplicate files inside a directory tree."""
 
from os import walk, remove, stat
from os.path import join as joinpath
from pathlib import Path, PurePath, PurePosixPath
from hashlib import md5
import argparse
from argparse import ArgumentParser
import os
import hashlib
import shutil

accepted_image_formats = ['.JPG','.PNG']
accepted_movie_formats = ['.AVI', '.MOV']
accepted_formats = accepted_image_formats + accepted_movie_formats
print(accepted_formats)

def output_folder(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def hashfile(path, blocksize = 65536):
    afile = open(path, 'rb')
    hasher = hashlib.md5()
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    afile.close()
    return hasher.hexdigest()
 
def find_duplicates( rootdir, year ):
    """Find duplicate files in directory tree."""
    file_list = []

    outfolder = "e:\\Pictures\\final_" +  year

    if not os.path.exists(outfolder):
        os.makedirs(outfolder)

    for dirpath, dirnames, filenames in os.walk( rootdir ):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)  
            if os.path.basename(dirpath).startswith(year):
                file_extension = PurePosixPath(file_path).suffix
                if file_extension in accepted_formats:     
                    file_list.append(file_path)
                    
    unique = set()
    duplicates = []

    with open("duplicates" + year + ".txt", "w") as f:
        for filepath in file_list:
            filehash = hashfile(filepath)
            if filehash not in unique:
                
                only_filename = os.path.basename(filepath)
                # shutil.move(filepath, os.path.join(outfolder, only_filename))
                unique.add( filehash )
            else:
                f.write(filepath + '\n')
                duplicates.append( filepath )
    return duplicates
 
if __name__ == '__main__':
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--folder", required = True,
        help = "path to input folder containing subfolders and images")
    ap.add_argument("-y", "--year", required = True,
        help = "path to input folder containing subfolders and images")
    args = vars(ap.parse_args())

    find_duplicates(args['folder'], args['year'])

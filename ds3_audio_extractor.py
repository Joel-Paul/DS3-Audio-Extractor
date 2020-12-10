#! /usr/bin/env python3

""" A Program that extracts sound files from Dark Souls 3.

Joel Paul
2020-12-10 (YYYY-MM-DD)
"""

import os
import sys
import subprocess
import argparse
import tkinter as tk
from tkinter import filedialog
from time import perf_counter, sleep


HELP = "Dark Souls 3 Audio Extracting Tool. "\
        + "If no arguments apart from --input and --output are specified, all options will run by default. "\
        + "If an argument other than --input/--output is passed, the rest will become False by default. "\
        + "(e.g. if --decrypt and --extract are passed, --unpack and --split will be False by default.)"
# Paths
CWD = os.getcwd()
INITIAL_DS3_PATH = os.path.join('C:', 'Program Files (x86)', 'Steam', 'steamapps', 'common', 'DARK SOULS III', 'Game')
# External programs.
FSB_EXT = os.path.join(CWD, 'dependencies', 'fsbext.exe')
FSB5_SPLIT = os.path.join(CWD, 'dependencies', 'fsb5_split.exe')
FSB_AUD_EXTR = os.path.join(CWD, 'dependencies', 'fsb_aud_extr.exe')
BINDER_TOOL = os.path.join(CWD, 'dependencies', 'BinderTool.v0.5.2', 'BinderTool.exe')
# '*.bdt' files we want (ignore the rest).
WANTED_DATA = ('Data1.bdt', 'Data5.bdt', 'DLC1.bdt', 'DLC2.bdt')


# Global variables.
# (I know, I'm not proud about it either.)
raw_path = ''
wav_path = ''
sound_path = ''
output_path = os.path.join(CWD, 'output')
DS3_path = INITIAL_DS3_PATH


def main():
    global DS3_path
    global output_path

    unpack = False
    decrypt = False
    split = False
    extarct = False

    # Initialise parser.
    parser = argparse.ArgumentParser(description=HELP)
    # Add arguments.
    parser.add_argument("-i", "--input",\
            help="Path to the folder containing 'DarkSoulsIII.exe'. (Defaults to the default Steam installation folder)")
    parser.add_argument("-o", "--output",\
            help="Path to output location. (Defaults to the 'output' folder in the current directory).")
    parser.add_argument("-u", "--unpack", action='store_true',\
            help="Unpacks '*.bdt' files from the Dark Souls 3 directory.")
    parser.add_argument("-d", "--decrypt", action='store_true',\
            help="Decrypts '*.fsb' files from the Dark Souls 3 '\sound' directory.")
    parser.add_argument("-s", "--split", action='store_true',\
            help="Splits multitrack '*.fsb' files into individual '*.fsb' files. Requires unpacked and/or decrypted files.")
    parser.add_argument("-e", "--extract", action='store_true',\
            help="Extracts audio files from split '*.fsb' files into '*.wav' format.")
    
    # Read from command line.
    args = parser.parse_args()
    if args.input:
        DS3_path = args.input
    if args.output:
        output_path = args.output
    unpack = args.unpack
    decrypt = args.decrypt
    split = args.split
    extract = args.extract
    
    # If none of these arguments were specified, run them all by default.
    if (not (unpack or decrypt or split or extract)):
        unpack = True
        decrypt = True
        split = True
        extract = True
    
    # If no arguments were specified, ask the user what they want to do.
    if len(sys.argv) == 1:
        run = False
        print('"Welcome, ashen one."')
        while not run:
            print("\nCommands:")
            print("\tr/run - Run the program using the current configuration.")
            print("\to/output - Change the output location. Defaults to '\output'.")
            print("\ta/about - About this program.")
            print("\tx/exit - Exit this program.")
            
            print("Configuration:")
            print("\tu/unpack - Unpack '*.bdt' files from the Dark Souls 3 directory. ({})".format(unpack))
            print("\td/decrypt - Decrypt '*.fsb' files from the Dark Souls 3 '\sound' directory. ({})".format(decrypt))
            print("\ts/split - Split unpacked/decrypted multitrack '*.fsb' files into individual '*.fsb' files. ({})".format(split))
            print("\te/extract - Extract audio files from split '*.fsb' files into '*.wav' format. ({})".format(extract))

            command = input('\n"Speak thine heart\'s desire": ').lower()
            if command in ['r', 'run']:
                run = True
            elif command in ['o', 'output']:
                root = tk.Tk()
                root.withdraw()  # Hide tkinter window.
                output_path = ''
                while (output_path == ''):
                    output_path = tk.filedialog.askdirectory(title="Select Output Directory", initialdir=CWD)
                print("Output path set to {}".format(output_path))
            elif command in ['a', 'about']:
                print("This program simply combines existing tools to create an easy experience "\
                      + "in extracting the audio from Dark Souls III.\n")
                print("Credits:")
                print("Creator of this program: Joel Paul")
                print("Creator of 'BinderTool.exe': 'Atvaark' (https://github.com/Atvaark/BinderTool)")
                print("Creator of 'fsbext.exe': Luigi Auriemma (http://www.aluigi.altervista.org/papers.htm#fsbext)")
                print("Creator of 'fsb5_split.exe': Naram 'CyberBotX' Qashat (https://github.com/CyberBotX/fsb5_split)")
                print("Creator of 'fsb_aud_extr.exe': 'id-daemon' (https://zenhax.com/viewtopic.php?t=1901)")
            elif command in ['x', 'exit']:
                run = True
                unpack = False
                decrypt = False
                split = False
                extract = False

            elif command in ['u', 'unpack']:
                unpack = not unpack
                print("Unpack is now set to {}.".format(unpack))
            elif command in ['d', 'decrypt']:
                decrypt = not decrypt
                print("Decrypt is now set to {}.".format(decrypt))
            elif command in ['s', 'split']:
                split = not split
                print("Split is now set to {}.".format(split))
            elif command in ['e', 'extract']:
                extract = not extract
                print("Extract is now set to {}.".format(extract))
            else:
                print('"I am truly sorry ashen one, but I do not posses such abilities. '\
                    + 'Allow me to serve thee in other ways."')
    
    # Execute commands.
    if (unpack or decrypt or split or extract):
        print('\n"Very well. Then touch the data within me. Take nourishment from these sovereignless sounds..."\n')
        init_output(output_path)
    if unpack:
        unpack_data()
    if decrypt:
        decrypt_fsb()
    if split:
        split_data()
    if extract:
        extract_data()
    
    print('"Farewell, ashen one."')
    if len(sys.argv) == 1:
        input("Press enter to exit.")


def unpack_data():
    """ Unpacks '*.bdt' files from the Dark Souls 3 directory.

    This function uses 'BinderTool.exe' by 'Atvaark'.
    (https://github.com/Atvaark/BinderTool)
    """
    check_DS3_path()
    print('\t"Let these sounds, withdrawn from their vessels,\n\tManisfestations of disparity..."\n')
    print("[1/4] Unpacking '*.bdt' files (this will take ~15 minutes):")
    
    timer = perf_counter()
    for file in progressBar(list(os.scandir(DS3_path)), prefix='Progress:', suffix='Unpacked', length=40):
        # Check if this file has already been unpacked.
        unpacked_path = os.path.join(raw_path, os.path.basename(file).replace('.bdt', ''))
        is_unpacked = os.path.exists(unpacked_path)
        
        # Unpack any remaining files.
        if wanted_data(file) and not is_unpacked:
            unpack_cmd = '"{0}" "{1}" "{2}"'\
                    .format(BINDER_TOOL,
                    file.path, os.path.join(raw_path,
                    os.path.basename(file).replace('.bdt', '')))
            subprocess.call(unpack_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    elapsed_time = perf_counter() - timer
    print("Completed in {} seconds.\n".format(elapsed_time))


def decrypt_fsb():
    """ Decrypts '.fsb' files in the Dark Souls 3 'sound' directory.

    This function uses 'FSB files extractor' (fsbext.exe) by Luigi Auriemma.
    (http://www.aluigi.altervista.org/papers.htm#fsbext)
    """
    check_DS3_path()
    print('\t"Elucidated by current,\n\tBurrow deep within me..."\n')
    print("[2/4] Decrypting '*.fsb' files (this will take ~25 seconds):")

    DS3_sound_path = os.path.join(DS3_path, 'sound')
    
    timer = perf_counter()
    for file in progressBar(list(os.scandir(DS3_sound_path)), prefix='Progress:', suffix='Decrypted', length=40):
        # Check if this file has already been decrypted.
        decrypted_path = os.path.join(sound_path, os.path.basename(file).replace('.fsb', '_crypt.fsb'))
        is_decrypted = os.path.isfile(decrypted_path)
        
        # Decrypt any remaining files.
        if (file.path.endswith('.fsb') and file.is_file() and not is_decrypted):
            decrypt_cmd = '"{0}" -e FDPrVuT4fAFvdHJYAgyMzRF4EcBAnKg 1 -d "{1}" "{2}"'\
                .format(FSB_EXT, sound_path, file.path)
            subprocess.call(decrypt_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    elapsed_time = perf_counter() - timer
    print("Completed in {} seconds.\n".format(elapsed_time))


def split_data():
    """ Splits decrypted '.fsb' files in all folders.
    """
    print('\t"Retreating to a directory beyond the reach of data,\n\tLet them assume a new master..."\n')
    print("[3/4] Splitting '*.fsb' files (this will take ~1.5 minutes):")
    
    timer = perf_counter()
    for folder in progressBar(list(os.scandir(raw_path)), prefix='Progress:', suffix='Split', length=40):
        # Some folders have their '*.fsb' files in a sound directory,
        # so this takes care of that.
        if os.path.exists(os.path.join(folder.path, 'sound')):
            fsb_path = os.path.join(folder.path, 'sound')
        else:
            fsb_path = folder.path
        split_fsb(fsb_path)
        
    elapsed_time = perf_counter() - timer
    print("Completed in {} seconds.\n".format(elapsed_time))


def extract_data():
    """ Extract audio files in '.wav' format from split '.fsb' files from multiple folders.
    """
    print('\t"Inhabiting \'*.wav\', casting themselves upon new forms..."\n')
    print("[4/4] Extracting '*.fsb' files (this will take ~2 hours):")

    timer = perf_counter()
    i = 1
    for folder in os.scandir(raw_path):
        if os.path.exists(os.path.join(folder.path, 'sound')):
            fsb_path = os.path.join(folder.path, 'sound')
        else:
            fsb_path = folder.path
        print('\t[{0}/{1}] Extracting from {2}'\
                  .format(i, len(list(os.scandir(raw_path))), os.path.basename(folder.path)))
        extract_fsb(fsb_path)
        i += 1
        
    elapsed_time = perf_counter() - timer
    print("Completed in {} seconds.\n".format(elapsed_time))


def split_fsb(fsb_dir):
    """ Splits decrypted '.fsb' files.

    This function uses a program made by Naram 'CyberBotX' Qashat.
    (https://github.com/CyberBotX/fsb5_split)
    """
    for file in os.scandir(fsb_dir):
        # Check if this file has already been split.
        split_path = os.path.join(fsb_dir, os.path.basename(file).replace('.fsb', ''))
        is_split = os.path.exists(split_path)

        # Split any remaining files.
        if (file.path.endswith('.fsb') and not is_split):
            split_cmd = '"{0}" "{1}"'.format(FSB5_SPLIT, file.path)
            subprocess.call(split_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def extract_fsb(fsb_dir):
    """ Extract audio files in '.wav' format from split '.fsb' files.

    This function uses 'fsb_aud_extr.exe' by 'id-daemon'.
    (https://zenhax.com/viewtopic.php?t=1901)
    """
    for folder in progressBar(list(os.scandir(fsb_dir)), prefix='Progress:', suffix='Extracted', length=40):
        if folder.is_dir():
            for file in os.scandir(folder.path):
                # Check if this file has already been extracted.
                extracted_path = os.path.join(wav_path, os.path.relpath(folder.path, raw_path),\
                        os.path.basename(file).replace('.fsb', '.wav'))
                is_extracted = os.path.isfile(extracted_path)
                
                # Extract audio.
                if (file.path.endswith('.fsb') and not is_extracted):
                    # Change working directory to output location.
                    # 'fsb_aud_extr.exe' does not have an output option (afaik),
                    # and just outputs at the current working directory,
                    # so by changing it we can change where the files are output.
                    output_dir = os.path.join(wav_path, os.path.relpath(folder.path, raw_path))
                    if not os.path.exists(output_dir):
                        os.makedirs(output_dir)
                    os.chdir(output_dir)
                    
                    extract_cmd = '"{0}" "{1}"'.format(FSB_AUD_EXTR, file.path)
                    subprocess.call(extract_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # Change back just as a sanity check.
    os.chdir(CWD)


def check_DS3_path():
    """ Check if the current DS3_path is valid.

    If not valid and there are no arguments, prompt the user
    to provide the proper location.
    Otherwise print that it is not found and carry on as usual.
    """
    global DS3_path
    root = tk.Tk()
    root.withdraw()  # Hide tkinter window.
    
    while not os.path.isfile(os.path.join(DS3_path, 'DarkSoulsIII.exe')):
        if len(sys.argv) == 1:
            print("Please provide the directory to 'DarkSoulsIII.exe'.\n")
            DS3_path = tk.filedialog.askdirectory(title="Select Dark Souls 3 Install Location", initialdir=INITIAL_DS3_PATH)
        else:
            print("'DarkSoulsIII.exe' not found.\n")
            break


def init_output(path):
    """ Initialise path based on 'output_path'.
    """
    global output_path
    global raw_path
    global wav_path
    global sound_path
    
    output_path = path
    raw_path = os.path.join(output_path, 'raw')
    wav_path = os.path.join(output_path, 'wav')
    sound_path = os.path.join(raw_path, 'sound')

    # Make dirs if they don't exist.
    if (not os.path.exists(output_path)):
        os.makedirs(output_path)
    if (not os.path.exists(raw_path)):
        os.makedirs(raw_path)
    if (not os.path.exists(wav_path)):
        os.makedirs(wav_path)
    if (not os.path.exists(sound_path)):
        os.makedirs(sound_path)


def wanted_data(file):
    """ Check if the passed file is wanted.

    Not all '*.bdt' files contain audio, so those
    should be skipped to save time and space.
    """
    for data in WANTED_DATA:
        if os.path.basename(file) == data:
            return True
    return False


def progressBar(iterable, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """ Provides a progress bar for iterable stuff.

    This function was made by StackOverflow user Greenstick.
    (https://stackoverflow.com/a/34325723)
    """
    
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    total = len(iterable)
    # Progress Bar Printing Function
    def printProgressBar (iteration):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Initial Call
    printProgressBar(0)
    # Update Progress Bar
    for i, item in enumerate(iterable):
        yield item
        printProgressBar(i + 1)
    # Print New Line on Complete
    print()

if __name__ == '__main__':
    main()

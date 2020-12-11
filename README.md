# Dark Souls III Audio Extractor #
This Python script makes it easy to extract the audio from Dark Souls 3 into '\*.wav' format. It utilises existsing tools to extract the data, all this script does is combine them all together.

## Installation ##
To install and run this project you will need to also download some external programs.
* First download/clone `ds3_audio_extractor.py` into your chosen directory.
* In the same directory create a folder called `dependencies`.
* Go to https://github.com/Atvaark/BinderTool/releases and download `BinderTool.v0.5.2.zip`. Extract this into the dependencies directory. The path to `BinderTool.exe` should look something like `.../dependencies/BinderTool.v0.5.2/BinderTool.exe`.
* Go to http://www.aluigi.altervista.org/papers.htm#fsbext and download 'FSB files extractor 0.3.8'. Drag and drop `fsbext.exe` into the `dependencies` folder.
* Go to https://github.com/CyberBotX/fsb5_split and compile the source. Rename the compiled program to `fsb5_split.exe` and drop it into the `dependencies` folder.
* Go to https://zenhax.com/viewtopic.php?t=1901 and download `fmod_extractors.rar` and `fmod_dlls.rar`. Extract `fsb_aud_extr.exe` and `fmodL.dll` into the `dependencies` folder.
* Your `dependencies` folder should look like the image below:

## How to Use ##
You can either double-click the Python file or run it through the command line.
Double-clicking will allow you to choose what configuration you want to run the program in. If you are running it for the first time, simply press `r` to run the script. (__Be aware that this may take around 2.5 hours to complete__).

You can use the following arguments to run the script from the command line:
```usage: ds3_audio_extractor.py [-h] [-i INPUT] [-o OUTPUT] [-u] [-d] [-s] [-e]

Dark Souls 3 Audio Extracting Tool. If no arguments apart from --input and --output are specified, all options will
run by default. If an argument other than --input/--output is passed, the rest will become False by default. (e.g. if
--decrypt and --extract are passed, --unpack and --split will be False by default.)

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Path to the folder containing 'DarkSoulsIII.exe'. (Defaults to the default Steam installation
                        folder)
  -o OUTPUT, --output OUTPUT
                        Path to output location. (Defaults to the 'output' folder in the current directory).
  -u, --unpack          Unpacks '*.bdt' files from the Dark Souls 3 directory.
  -d, --decrypt         Decrypts '*.fsb' files from the Dark Souls 3 '\sound' directory.
  -s, --split           Splits multitrack '*.fsb' files into individual '*.fsb' files. Requires unpacked and/or
                        decrypted files.
  -e, --extract         Extracts audio files from split '*.fsb' files into '*.wav' format.
```

## Notes ##
The script will not unpack/decrypt/split/extract files if they have already have had that action applied to them (i.e. a file won't be decrypted if it already has been decrypted).

## Credits ##
* Creator of 'BinderTool.exe': 'Atvaark' (https://github.com/Atvaark/BinderTool)
* Creator of 'fsbext.exe': Luigi Auriemma (http://www.aluigi.altervista.org/papers.htm#fsbext)
* Creator of 'fsb5_split.exe': Naram 'CyberBotX' Qashat (https://github.com/CyberBotX/fsb5_split)
* Creator of 'fsb_aud_extr.exe': 'id-daemon' (https://zenhax.com/viewtopic.php?t=1901)
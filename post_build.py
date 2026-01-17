# Simple python script used to
# copy some libraries to the "target" directory
# after Rust build
# Note that Rust build should be run via "cargo make <cmd>" command
# in order to automate all the compile process
import os
from pathlib import Path
import shutil
import sys

# some config vars
# format: (source, destination_name)
SOURCE = (
    ("resources/commands/", "resources/commands/"),
    ("resources/vosk/", "resources/vosk/"),
    ("resources/lib/", "lib/"),
    ("resources/keywords/", "resources/keywords/"),
    ("resources/rustpotter/", "resources/rustpotter/"),
    ("resources/sound/", "resources/sound/"),
    ("lib/windows/amd64/libgcc_s_seh-1.dll", None),
    ("lib/windows/amd64/libstdc++-6.dll", None),
    ("lib/windows/amd64/libvosk.dll", None),
    ("lib/windows/amd64/libvosk.lib", None),
    ("lib/windows/amd64/libwinpthread-1.dll", None)
)

TARGET_DIRS = (
    "target/debug",
    "target/release"
)

ABS_PATH = os.getcwd() + "/"

# check for force flag
force_overwrite = "-force" in sys.argv

for tdir in TARGET_DIRS:
    tdir = ABS_PATH + tdir

    if not Path(tdir).is_dir():
        print("Skipping target, not a directory: ", tdir)
        continue

    # copy lib files
    for entry in SOURCE:
        if isinstance(entry, tuple):
            src, dest_name = entry
        else:
            src, dest_name = entry, None

        src_path = ABS_PATH + src

        if os.path.isdir(src_path):
            # copy the whole directory
            target_name = dest_name if dest_name else os.path.basename(src.rstrip('/'))
            full_target_dir_path = os.path.join(tdir, target_name)
            
            if os.path.isdir(full_target_dir_path):
                if force_overwrite:
                    shutil.rmtree(full_target_dir_path)
                    shutil.copytree(src_path, full_target_dir_path)
                    print("[+] Directory overwritten: ", src, "->", target_name)
                else:
                    print("[-] Directory already exists, skipping: ", src, "->", target_name)
            else:
                shutil.copytree(src_path, full_target_dir_path)
                print("[+] Directory copied: ", src, "->", target_name)

        elif os.path.isfile(src_path):
            # copy file
            target_name = dest_name if dest_name else os.path.basename(src)
            full_target_file_path = os.path.join(tdir, target_name)
            
            if os.path.isfile(full_target_file_path):
                if force_overwrite:
                    os.remove(full_target_file_path)
                    shutil.copy(src_path, full_target_file_path)
                    print("[+] File overwritten: ", src, "->", target_name)
                else:
                    print("[-] File already exists, skipping: ", src, "->", target_name)
            else:
                shutil.copy(src_path, full_target_file_path)
                print("[+] File copied: ", src, "->", target_name)
        else:
            print("[?] Unknown entity to copy: ", src)

    print("Post compile build done.")

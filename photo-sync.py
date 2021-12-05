from argparse import ArgumentParser
from os import path, makedirs, walk
from re import compile
from shutil import copy2

if __name__ == "__main__":
    parser = ArgumentParser(description='Copy local files to network attached storage', epilog='example: python .\photo-sync.py --local "C:\Pictures" --nas "\\\\nas\Photos\\2021"')
    parser.add_argument('--local', required=True, type=str, help='Local directory')
    parser.add_argument('--nas', required=True, type=str, help='Network attached storage directory')
    args = parser.parse_args()

    # Only match JPEG files following my naming convention
    jpgRegex = compile('^(\d\d\d\d)(\d\d)(\d\d) \d\d\d\d\.jpe?g$')

    for root, dirPaths, filePaths in walk(args.local):
        for filePath in filePaths:
            match = jpgRegex.match(filePath)
            if match and len(match.groups()) == 3:
                year = match.group(1)
                month = match.group(2)
                day = match.group(3)

                parent = path.join(args.nas, f'{year}-{month}-{day}')
                makedirs(parent, exist_ok=True)

                source = path.join(root, filePath)
                print(f"Copying '{source}' to '{parent}'")
                copy2(source, parent, follow_symlinks=False)
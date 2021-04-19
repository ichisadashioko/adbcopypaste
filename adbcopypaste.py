import os
import sys
import argparse
import traceback

MAX_TEXT_FILE_SIZE = 5242880

parser = argparse.ArgumentParser()
parser.add_argument('file_path_or_str', action='store', type=str)
parser.add_argument('-s', '--serial', dest='serial', type=str)

args = parser.parse_args()

tmp_filepath = None

if len(args.file_path_or_str) == 0:
    print('file_path_or_str is empty!', file=sys.stderr)
    sys.exit(1)

if os.path.exists(args.file_path_or_str):
    if not os.path.isfile(args.file_path_or_str):
        print(args.file_path_or_str, 'is not a normal file!', file=sys.stderr)
        sys.exit(1)

    filesize = os.path.getsize(args.file_path_or_str)

    if filesize == 0:
        print(f'{args.file_path_or_str} is empty.', file=sys.stderr)
        sys.exit(1)
    elif filesize > MAX_TEXT_FILE_SIZE:
        print(f'{args.file_path_or_str} is too large ({filesize}). Maximum allowed size is {MAX_TEXT_FILE_SIZE}.', file=sys.stderr)
        sys.exit(1)

    with open(args.file_path_or_str, mode='r', encoding='utf-8') as infile:
        try:
            while True:
                line = infile.readline()
                if len(line) == 0:
                    break
        except UnicodeDecodeError:
            print(f'{args.file_path_or_str} is not an UTF-8 encoded text file!')
            sys.exit(1)
        except Exception as ex:
            traceback.print_exc(file=sys.stderr)
            sys.exit(-1)

    tmp_filepath = args.file_path_or_str
else:
    print(args.file_path_or_str, 'does not exist! I am treating it as string to be copied.')
    encoded_bytes = args.file_path_or_str.encode('utf-8')

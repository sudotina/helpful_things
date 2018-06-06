#!/usr/bin/env python
# Written By: sudotina

import os
import sys
import hashlib

files_list = {}


def main(directory):
    for root, dirs, files in os.walk(directory):
        for f in files:
            full_path = os.path.join(root, f)
            sha2 = hashlib.sha256(open(full_path, 'rb').read()).hexdigest()
            if sha2 in files_list.keys():
                files_list[sha2].append(full_path)
            else:
                files_list[sha2] = [full_path]

    for hash_num, files in files_list.iteritems():
        if len(files) > 1:
            print "{} are duplicates.".format(files)


if __name__ == "__main__":
    main(sys.argv[1])

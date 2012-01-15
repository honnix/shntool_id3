'''
Created on May 24, 2009

Write ID3 tags to mp3 files split by shntool.

Files split by shntool should be named like this: tracknumber--@artist--@album--@title.mp3, 
and encoding of file name should be 'utf-8'.

@author: honnix
@version: 0.1.0
'''

import sys
import os
import mutagen

from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3

def usage():
    print 'id3.py </path/to/directory>'

def main():
    separator = '--@'
    suffix = '.mp3'
    file_name_encoding = 'utf-8'

    if len(sys.argv) < 2:
        usage()
        sys.exit(-1)

    top_dir = sys.argv[1]
    mp3_files = os.listdir(top_dir)

    for mp3_file in mp3_files:
        if not mp3_file.endswith(suffix):
            print 'Not an mp3 file.'
            continue

        full_path = os.path.join(top_dir, mp3_file)
        mp3 = MP3(full_path, ID3 = EasyID3)

        try:
            mp3.add_tags(ID3 = EasyID3)
        except mutagen.id3.error:
            print '%s has already had tags.' % mp3_file

        id3_info = unicode(mp3_file[0:-4], file_name_encoding).split(separator)
        if len(id3_info) < 4:
            print 'Wrong file name. Should be tracknumber' + separator + 'artist' + \
            separator + 'album' + separator + 'title'
            continue

        mp3['tracknumber'] = id3_info[0]
        mp3['artist'] = id3_info[1]
        mp3['album'] = id3_info[2]
        mp3['title'] = id3_info[3]

        mp3.save()

        os.rename(full_path, os.path.join(top_dir, id3_info[3] + '.mp3'))

if __name__ == '__main__':
    main()

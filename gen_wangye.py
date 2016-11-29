# -*- coding=gbk -*-

import sys, getopt
import re
import os
from os.path import isfile, join, isdir, getsize

def is_video(filename):
    houzhui_list = [".mp4", ".avi", ".mkv", ".flv", ".rmvb", ".wmv"]
    for houzhui in houzhui_list:
        if filename.endswith(houzhui):
            return True
    return False
    
def get_url_list(file_path, url_list):
    if isfile(file_path):
        if is_video(file_path):
            url_list.append("/".join(file_path.split("\\")[2:]))
    elif isdir(file_path):
        for filename in os.listdir(file_path):
            get_url_list(join(file_path, filename), url_list)
        

def work(ff = sys.stdin, fout = sys.stdout):
    input_path="F:\\aaa"
    url_list = []
    get_url_list(input_path, url_list)
    s = ""
    for line in ff:
        line = line.rstrip("\n")
        if line.endswith("###urls###"):
            for i, url in enumerate(url_list):
                fout.write(("url[%i] = \"%s\"\n" %(i, url)).decode("gbk").encode("utf8"))
        else:
            fout.write(("%s\n" %(line)).decode("gbk").encode("utf8"))
#     for line in ff:
#         line = line.rstrip("\n")
#         splits = line.split("\t")

def main(args):
    ff = sys.stdin
    fout = sys.stdout
    opts, args = getopt.getopt(args, "f:o:")
    for op, value in opts:
        if op == '-f':
            ff = open(value, 'r')
        if op == '-o':
            fout = open(value, 'w')
    work(ff, fout)

if __name__ == '__main__':
    main(sys.argv[1:])
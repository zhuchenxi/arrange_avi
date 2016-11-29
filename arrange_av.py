# -*- coding=gbk -*-

import sys, getopt
import re
import os
import urllib2
from os.path import isfile, join, isdir, getsize

def canbe_played(filename):
    houzhui_list = [".mp4", ".avi", ".mkv", ".flv", ".rmvb", ".wmv"]
    for houzhui in houzhui_list:
        if filename.endswith(houzhui):
            return True, houzhui
    return False, None

def search_fanhao(filename):
    r = re.search("[a-zA-Z]{2,}\-?[0-9]{3,}", filename)
    if not r is None:
        return r.group(0)
    return None

def get_av_pic(fanhao):
    print fanhao
    search_url = "https://avmo.pw/cn/search/%s" %(fanhao)
    req = urllib2.Request(search_url)
    flag = False
    for i in range(3):
        try:
            response = urllib2.urlopen(req)
            flag = True
            break
        except:
            continue
    if not flag:
        return None
    the_page = response.read()
    r = re.search("a class\=\"movie-box\" href\=\"(.*?)\"", the_page)
    if r is None:
        return None
    
    av_url = r.group(1)
    req = urllib2.Request(av_url)
    flag = False
    for i in range(3):
        try:
            response = urllib2.urlopen(req)
            flag = True
            break
        except:
            continue
    if not flag:
        return None
    the_page = response.read()
    r = re.search("img src\=\"(.*?)\"", the_page)
    if r is None:
        return None
    
    pic_url = r.group(1)
    hdr = {'User-Agent':'Mozilla/5.0'}
    req = urllib2.Request(pic_url, headers=hdr)
    flag = False
    for i in range(3):
        try:
            response = urllib2.urlopen(req)
            flag = True
            break
        except:
            continue
    if not flag:
        return None
    data = response.read()
    filename = "%s.jpg" %(fanhao)
    with open(filename, "wb") as f:
        f.write(data)
    return filename

def deal_file(filename, input_path, output_path):
    #print filename
    ret, houzhui = canbe_played(filename)
    if not ret:
        return False
    #print filename
    fanhao = search_fanhao(filename)
    #print fanhao
    pic = get_av_pic(fanhao)
    if pic is None:
        return False
    ret = os.system("mkdir %s\\%s" %(output_path, fanhao))
    if ret != 0:
        return False
    new_name = "%s%s" %(fanhao, houzhui)
    new_path = "%s\\%s\\" %(output_path, fanhao)
    #os.system(r"move %s\\\"%s\" %s" %(input_path, filename, new_path))
    
    #print r"move %s %s" %(join(input_path, filename), new_path)
    #print r"move %s\\\"%s\" %s" %(input_path, filename, new_path)
    os.system("move \"%s\" \"%s\"" %(pic, new_path))
    os.system("move \"%s\" \"%s%s\"" %(join(input_path, filename), new_path, new_name))
    return True

def work(ff = sys.stdin, fout = sys.stdout):
    #设置代理
    #proxy=urllib2.ProxyHandler({'https': 'my_daili'})
    #opener=urllib2.build_opener(proxy)
    #urllib2.install_opener(opener)
    
    #设置输入输出路径
    input_path = "F:\\a备份"
    #input_path = "F:\\aaa\\自动化空间test"
    output_path = "F:\\aaa\\lenovo剩余"
    
    for filename in os.listdir(input_path):
        if isfile(join(input_path, filename)):
            deal_file(filename, input_path, output_path)
            
        elif isdir(join(input_path, filename)): #文件夹的情况
            sub_path = join(input_path, filename)
            max_du = -1
            max_name = None
            for sub_filename in os.listdir(sub_path):
                if isdir(join(sub_path, sub_filename)):
                    continue
                du_size =  getsize(join(sub_path, sub_filename))
                if du_size > max_du:
                    max_du = du_size
                    max_name = sub_filename
                if max_du == -1:
                    continue
            #print "%s\t%i" %(max_name, max_du)
            #print sub_path
            if max_du == -1:
                continue
            ret = deal_file(max_name, sub_path, output_path)
            if ret:
                fout.write("%s\n" %sub_path)
                fout.flush()

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

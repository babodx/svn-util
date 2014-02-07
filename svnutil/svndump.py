#!/usr/bin/python
# -*- coding: utf-8 -*-

#  _   _       _ _                     _
# | | | | ___ | | |__  _ __ ___   ___ | | __
# | |_| |/ _ \| | '_ \| '__/ _ \ / _ \| |/ /
# |  _  | (_) | | |_) | | | (_) | (_) |   <
# |_| |_|\___/|_|_.__/|_|  \___/ \___/|_|\_\
# wanghaikuo@gmail.com


from optparse import OptionParser
import os
import string
import re
import datetime

def list_repositories(root):
    repo_list= {}
    if(not os.path.isdir(root)):
        return repo_list

    list_dirs = os.listdir(root)
    for repo in list_dirs:
        file = root + os.sep + repo
        if(os.path.isdir(file)):
            current = file + os.sep + "db" + os.sep + "current"
            if(os.path.isfile(current)):
                cmd = "cat "+ current + "|awk '{print $1}'"
                version = os.popen(cmd).readline()
                version = string.atoi(version)
                repo_list[repo]= version
    #print repo_list
    return repo_list


def last_revision(repo_name,dest_path):
    print repo_name,dest_path
    revision = -1;

    pattern = repo_name+'_\d{4}-\d{2}-\d{2}_r\d{1,100}-\d{1,100}.bz2'

    for file in os.listdir(dest_path):
        if not os.path.isfile(dest_path + os.sep+file):
            continue

        result = re.match(pattern,file)
        if result == None:
            continue
        index = file.rindex('-')+1

        value = file[index:-4]

        value = string.atoi(value)
        if value>revision:
            revision = value
    return revision


def full_backup(repo_name,root, dest_path,last):
    file_name = '%s_%s_r0-%d'%(repo_name,str(datetime.date.today()),last)

    print u"全备份svn库:"+repo_name
    os.system('rm -f '+root+os.sep+repo_name+'_*')
    os.system('svnadmin dump --deltas '+root+os.sep+repo_name + '|bzip2 |tee '+ dest_path+os.sep+file_name + '.bz2 | md5sum > '+dest_path+os.sep+file_name+'.md5')


def incerese_backup(repo_name, src_path,dest_path,from_revision,to_revision):
    print u"增量备份svn库："+repo_name+ 'r_'+from_revision+'-'+to_revision

    file_name = '%s_%s_r%d-%d'%(repo_name,str(datetime.date.today()),from_revision,to_revision)
    print 'svnadmin dump --deltas '+src_path + os.sep + repo_name + \
        '-r'+from_revision+':'+ to_revision+ \
        ' --incremental |bzip2 |tee '+ dest_path+os.sep+file_name + \
        '.bz2 | md5sum > '+dest_path+os.sep+file_name+'.md5'


def main():
    parser= OptionParser(
        # prog=u"svndump [-f] svn仓库路径 备份目录",usage="%prog",
        # description=u'将{svn仓库路径}下的所有svn库备份到{备份目录}。'+
        #             u'默认为增量备份：根据{备份目录}中已有备份文件的名称中记录的revision和各svn库的当前revision进行增量备份；'+
        #             u'如果{备份目录}中没有某个svn库的备份文件，则自动执行全备份。也可以使用`-f`参数强制执行全备份。'+
        #             u'备份文件的命名规则为{svn库名称}_yyyy-mm-dd_r{start_revision}-{end_revision}.bz2.'
        prog = 'svndump.py [-f] SVN_REPOs_ROOT DEST_DIR', usage='%prog',
        description= 'default formmat: {REPO_NAME}_yyyy-mm-dd_r{start_revision}-{end_revision}.bz2'
        )

    parser.add_option("-f", dest="full", action="store_true" , default = False, help=u"进行全备份")


    (options, args) = parser.parse_args()

    if len(args)==2:
        src_path = args[0]
        dest_path = args[1]

        repo_list = list_repositories(src_path)

        if(len(repo_list)==0):
            print src_path +" 不是有效的svn仓库根目录!"
            exit(-1)

        if(not os.path.isdir(dest_path)):
            print dest_path +" 不是有效的备份目录!"
            exit(-2)


        if(options.full):
            for repo in repo_list:
                full_backup(src_path + os.sep + repo, dest_path,repo_list.get(repo))
        else:
            for repo in repo_list:
                last = last_revision(repo,dest_path)
                if last == repo_list.get(repo):
                    print 'svn库['+repo+']没有更新，不需要增量备份！'
                    continue
                if last == -1:
                    full_backup(repo, src_path ,dest_path,repo_list.get(repo))
                else:
                    incerese_backup(repo,src_path, dest_path , last+1, repo_list.get(repo))

    else:
        parser.print_help()


if __name__=="__main__":
    main()

# GitBook-auto-summary
Automatically update `SUMMARY.md` of a GitBook repo，default Based on the markdown title, not the article name，But if without a title, article name is used instead.


##  1. 背景

我们了解 gitbook plugin summary 自动生成 summary.md 文件内容
这是`book sm`命令依赖markdown文章名字组成目录结构的样子。

```bash
$ npm install gitbook-plugin-summary
$ npm install -g gitbook-summary
$ book sm
Finished, generated 'SUMMARY.md' successfully.
$ cat SUMMARY.md 
# Git Handbook

- Git
  * [2 Git Practice](Git/2_git_practice.md)
- Gitbook
  * [1 Gitbook Start](Gitbook/1_gitbook_start.md)
  * [2 Gitbook Plugin Summary](Gitbook/2_gitbook-plugin-summary.md)
  * [3 Github Pages Gitbook](Gitbook/3_github_pages_gitbook.md)
- Github
  * [1 Github Introduce](Github/1_github_introduce.md)
  * [2 Github Local Pull Github](Github/2_github_local_pull_github.md)
  * [3 Github Action](Github/3_github_action.md)
  * [4 Github Page](Github/4_github_page.md)
- Gitlab
  * [1 Gitlab Start](Gitlab/1_gitlab_start.md)
  * [2 Gitlab Deploy](Gitlab/2_gitlab_deploy.md)
  * [3 Gitlab Config](Gitlab/3_gitlab_config.md)
  * [4 Gitlab Runner Deploy](Gitlab/4_gitlab_runner_deploy.md)
  * [5 Gitlab Runner Management](Gitlab/5_gitlab_runner_management.md)
```
但我的需求是可以依据文章标题来生成整个结构，因为如果你有一批大量的markdown文章一个一个手写改动、添加、删除都是一件非常麻烦的事。

我发现来自[mofhu/GitBook-auto-summary](https://github.com/mofhu/GitBook-auto-summary)的功能接近我的需求。

```bash
 $ python3 gitbook-auto-summary.py -h
usage: gitbook-auto-summary.py [-h] [-o] [-a] directory

positional arguments:
  directory        the directory of your GitBook root

optional arguments:
  -h, --help       show this help message and exit
  -o, --overwrite  overwrite on SUMMARY.md
  -a, --append     append on SUMMARY.md
```
功能：
1. 可以通过`-o`覆盖已有的`SUMMARY.md`
2. 新生成一个`SUMMARY-GitBook-auto-summary.md`
3. 还可以通过-a实现追加内容。

##  2. 需求

但这离我渴望的需求还差一点点，那就是当文章内容存在标题，我更选择它来做链接名片，当不存在标题再去依赖文章名字（英文或中文）作为链接名片。并且在`gitbook-auto-summary.py`脚本当前目录我还可以让一些无关的目录作为例外。比如：`node_modules`

我把它实现了。

## 3. 代码
代码：[@ghostwritten/GitBook-auto-summary](https://github.com/Ghostwritten/GitBook-auto-summary)

```bash
# -*- coding: utf-8 -*-
# Author Frank Hu & zong xun
# GitBook auto summary
# summary all .md files in a GitBook folder

import argparse
import os
import re

teshu_list = ['_book', 'node_modules', 'img']

def output_markdown(dire, base_dir, output_file, append, iter_depth=0):
    """Main iterator for get information from every file/folder

    i: directory, base directory(to calulate relative path), 
       output file name, iter depth.
    p: Judge is directory or is file, then process .md/.markdown files.
    o: write .md information (with identation) to output_file.
    """
    top_list = os.listdir(dire)
    for i in top_list:
       if i in teshu_list:
          top_list.remove(i)

    for filename in sort_dir_file(top_list, base_dir): 
        # add list and sort
#        print('Processing ', filename) # output log
        file_or_path = os.path.join(dire, filename)
        if os.path.isdir(file_or_path): #is dir
            if mdfile_in_dir(file_or_path):
                # if there is .md files in the folder, output folder name
                output_file.write('  ' * iter_depth + '- ' + filename + '\n')
                print('  ' * iter_depth + '- ' + filename + '\n')
                output_markdown(file_or_path, base_dir, output_file, append, 
                                iter_depth + 1) # iteration
        else: # is file
            if is_markdown_file(dire, base_dir,filename): 
            # re to find target markdown files, $ for matching end of filename
                if (filename not in ['SUMMARY.md', 
                                     'SUMMARY-GitBook-auto-summary.md'] 
                    or iter_depth != 0): # escape SUMMARY.md at base directory
                    output_file.write('  ' * iter_depth + 
                        '- [{}]({})\n'.format(write_md_filename(dire, base_dir,filename, 
                                                                append), 
                            os.path.join(os.path.relpath(dire, base_dir), 
                                         filename)))
                    print('  ' * iter_depth + '- [{}]({})\n'.format(write_md_filename(dire, base_dir,filename, append), os.path.join(os.path.relpath(dire, base_dir),filename)))
                    # iter depth for indent, relpath and join to write link.

def mdfile_in_dir(dire):
    """Judge if there is .md file in the directory

    i: input directory
    o: return Ture if there is .md file; False if not.
    """
    for root, dirs, files in os.walk(dire):
        for filename in files:
            if re.search('.md$|.markdown$', filename):
                return True
    return False


def markdown_title_name(dire, base_dir,filename):
    path_filename = os.path.join(os.path.relpath(dire, base_dir), filename)
    with open(path_filename) as f:
        firstline = f.readline().rstrip()

    #if not firstline.isalnum():
    if firstline == '' or firstline == '---':
      title = filename.split('.',1)[0]
    else:
      title = firstline.lower().strip()
      for i in range(0, len(title)):
        if not title[i].isalnum():
           title = title[0:i] + ' ' + title[i+1:]
      while '--' in title:
         title = title.replace('--', ' ')
    title = title.strip(' ')
    return title

def is_markdown_file(dire, base_dir,filename):
    """ Judge if the filename is a markdown filename

    i: filename
    o: filename without '.md' or '.markdown'
    """
    if (filename not in ['SUMMARY.md','SUMMARY-GitBook-auto-summary.md']):
        match = re.search('.md$|.markdown$', filename)
        if not match:
           return False
        elif len(match.group()) is len('.md'):
           md_title = markdown_title_name(dire, base_dir,filename)
           return md_title
        elif len(match.group()) is len('.markdown'):
           md_title = markdown_title_name(dire, base_dir,filename)
           return md_title

def sort_dir_file(listdir, dire):
    # sort dirs and files, first files a-z, then dirs a-z
    list_of_file = []
    list_of_dir = []
    for filename in listdir:
        if os.path.isdir(os.path.join(dire, filename)):
            list_of_dir.append(filename)
        else: 
            list_of_file.append(filename)
    for dire in list_of_dir:
        list_of_file.append(dire)
    return list_of_file  

def write_md_filename(dire, base_dir,filename, append):
    """ write markdown filename

    i: filename and append
    p: if append: find former list name and return
       else: write filename
    """
    if append:
        for line in former_summary_list:
            if re.search(filename, line):
                s = re.search('\[.*\]\(',line)
                return s.group()[1:-2]
                
        else:
            return is_markdown_file(dire, base_dir,filename)
    else:
        return is_markdown_file(dire, base_dir,filename)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--overwrite', 
                        help='overwrite on SUMMARY.md', 
                        action="store_true")
    parser.add_argument('-a', '--append', 
                        help='append on SUMMARY.md', 
                        action="store_true")
    parser.add_argument('directory', 
                        help='the directory of your GitBook root')
    args = parser.parse_args()
    overwrite = args.overwrite
    append = args.append
    dir_input = args.directory

    # print information
    print('GitBook auto summary:', dir_input, end = ' ')
    if overwrite:
        print('--overwrite', end = ' ')
    if append and os.path.exists(os.path.join(dir_input, 'SUMMARY.md')): 
        #append: read former SUMMARY.md
        print(os.listdir(dir_input))
        print('--append', end = ' ')
        global former_summary_list
        with open(os.path.join(dir_input, 'SUMMARY.md')) as f:
            former_summary_list = f.readlines()
            f.close()
    print()
    # output to flie
    if (overwrite == False and 
        os.path.exists(os.path.join(dir_input, 'SUMMARY.md'))):
        # overwrite logic
        filename = 'SUMMARY-GitBook-auto-summary.md'
    else:
        filename = 'SUMMARY.md'
    output = open(os.path.join(dir_input, filename), 'w')
    output.write('# Summary\n\n')
    output_markdown(dir_input, dir_input, output, append)

    print('GitBook auto summary finished:) ')
    return 0

if __name__ == '__main__':
    main()
```
我们验证它的效果。

##  4. demo

### 4.1  `SUMMARY.md` 添加文章
添加`README.md`
```bash
$ ls
gitbook-auto-summary.py  README.md
root@yourdomain:~/example/summary-demo# python3 gitbook-auto-summary.py .
GitBook auto summary: . 
- [序言](./README.md)

GitBook auto summary finished:) 
root@yourdomain:~/example/summary-demo# ls
gitbook-auto-summary.py  README.md  SUMMARY.md
root@yourdomain:~/example/summary-demo# cat SUMMARY.md 
# Summary

- [序言](./README.md)
```
###  4.2 `SUMMARY.md` 添加目录
创建`Git`目录，并新增格式`.md`与`.markdown`格式文章。
```bash
$ ls Git/
1_git_introduce.markdown  2_git_practice.md
//查看是否有标题
$ head -n 1 Git/1_git_introduce.markdown 
# git 介绍 
$ head -n 1 Git/2_git_practice.md 
# git 实践

$ python3 gitbook-auto-summary.py .
GitBook auto summary: . 
- [序言](./README.md)

- Git

  - [git 介绍](Git/1_git_introduce.markdown)

  - [git 实践](Git/2_git_practice.md)

GitBook auto summary finished:) 
root@yourdomain:~/example/summary-demo# ls
Git  gitbook-auto-summary.py  README.md  SUMMARY-GitBook-auto-summary.md  SUMMARY.md
```
注意默认情况下（`python3 gitbook-auto-summary.py .`）当已存在 `SUMMARY.md`，脚本不会破坏已有`SUMMARY.md`。而是会生成新的文件：`SUMMARY-GitBook-auto-summary.md` 

```bash
$ cat SUMMARY-GitBook-auto-summary.md 
# Summary

- [序言](./README.md)
- Git
  - [git 介绍](Git/1_git_introduce.markdown)
  - [git 实践](Git/2_git_practice.md)

$ cat SUMMARY.md 
# Summary

- [序言](./README.md)
```

###  4.3 `SUMMARY.md` 添加子目录
添加子目录并且添加一篇markdown文章。
```bash
ls Git/
1_git_introduce.markdown  2_git_practice.md  3_git_remote_repo.md  git_command
root@yourdomain:~/example/summary-demo# ls Git/git_command/
2_git_command.md
root@yourdomain:~/example/summary-demo# head -n 1 Git/git_command/2_git_command.md 
# git 命令
```
执行如下：

```bash
$ python3 gitbook-auto-summary.py -o .
$ cat SUMMARY.md 
# Summary

- [序言](./README.md)
- Git
  - [git 介绍](Git/1_git_introduce.markdown)
  - git_command
    - [git 命令](Git/git_command/2_git_command.md)
  - [git 实践](Git/2_git_practice.md)
```

### 4.4 `SUMMARY.md` 覆盖
如果你只想覆盖`SUMMARY.md` 而已。可以`python3 gitbook-auto-summary.py -o .`实现。

```bash
$ python3 gitbook-auto-summary.py -o  .
GitBook auto summary: . --overwrite 
- [序言](./README.md)

- Git

  - [git 介绍](Git/1_git_introduce.markdown)

  - [git 实践](Git/2_git_practice.md)

GitBook auto summary finished:) 
root@yourdomain:~/example/summary-demo# cat SUMMARY.md 
# Summary

- [序言](./README.md)
- Git
  - [git 介绍](Git/1_git_introduce.markdown)
  - [git 实践](Git/2_git_practice.md)
```

有些情况，你可能认为覆盖比较危险，但又不想备份它，只想在原有的基础上追加内容。我们可以`python3 gitbook-auto-summary.py -a .`实现。

###  4.5 `SUMMARY.md` 追加

在Git目录新添了一篇文章。
```bash
$ ls Git/
1_git_introduce.markdown  2_git_practice.md  3_git_remote_repo.md
```
并且我手动改一下 `SUMMARY.md` 内容做一个标记。把`git 介绍`改成`git xxx`

```bash
# Gitbook-Handbook

- [序言](./README.md)
- Git
  - [git xxx](Git/1_git_introduce.markdown)
  - [git 实践](Git/2_git_practice.md)

ls
Git  gitbook-auto-summary.py  README.md  SUMMARY.md
```
执行`python3 gitbook-auto-summary.py -a  .`，`SUMMARY.md`修改的`xxx`并没有被覆盖掉。
```bash
$ python3 gitbook-auto-summary.py -a  .
$ cat SUMMARY-GitBook-auto-summary.md 
# Summary

- [序言](./README.md)
- Git
  - [git xxx](Git/1_git_introduce.markdown)
  - [github 管理远程仓库](Git/3_git_remote_repo.md)
  - [git 实践](Git/2_git_practice.md)
```
如果直接在`SUMMARY.md`追加。执行如下：

```bash
$ python3 gitbook-auto-summary.py -a -o  .
$ cat SUMMARY.md 
# Summary

- [序言](./README.md)
- Git
  - [git xxx](Git/1_git_introduce.markdown)
  - [github 管理远程仓库](Git/3_git_remote_repo.md)
  - [git 实践](Git/2_git_practice.md)
```

当去掉`-a`参数，覆盖重新生成。

```bash
$ python3 gitbook-auto-summary.py  -o  .
$ cat SUMMARY.md 
# Summary

- [序言](./README.md)
- Git
  - [git 介绍](Git/1_git_introduce.markdown)
  - [github 管理远程仓库](Git/3_git_remote_repo.md)
  - [git 实践](Git/2_git_practice.md)
```

### 4.6  `SUMMARY.md`忽略
我们创建一个目录`img`，也许你会用来存储图片。

```bash
$ mkdir img

$ ls
Git  gitbook-auto-summary.py  img  README.md  SUMMARY.md
```
修改代码第十行列表添加`'img'`

```bash
 ignore_list = ['_book', 'node_modules', 'img']
```
执行如下：

```bash
$ python3 gitbook-auto-summary.py  -o  .
$ cat SUMMARY.md 
# Summary

- [序言](./README.md)
- Git
  - [git 介绍](Git/1_git_introduce.markdown)
  - [github 管理远程仓库](Git/3_git_remote_repo.md)
  - [git 实践](Git/2_git_practice.md)
```
大纲并没有收到影响。因为`img`目录已被当作例外。

### 4.7 `SUMMARY.md`替代
当markdown没有标题的时候，也就是说第一行内容为空，我们判断认定为标题不存在。`“#  xxxx”`在其他行并不会被发现。这个时候我们会默认以文章名字作为链接名片。

我们把`Git/git_commnad/2_git_command.md`文章第一行的标题去掉或者下移一行。

```bash
$ head -n 2 Git/git_command/2_git_command.md 
<空行>
# git 命令
```
执行如下：

```bash
$ python3 gitbook-auto-summary.py -o .
$ cat SUMMARY.md 
# Summary

- [序言](./README.md)
- Git
  - [git 介绍](Git/1_git_introduce.markdown)
  - git_command
    - [2_git_command](Git/git_command/2_git_command.md)
  - [github 管理远程仓库](Git/3_git_remote_repo.md)
  - [git 实践](Git/2_git_practice.md)
```
这也是最初`book sm`命令结果的样子。

---
参考链接：

 - [mofhu/GitBook-auto-summary](http://frank-the-obscure.me/GitBook-auto-summary/)


![在这里插入图片描述](https://img-blog.csdnimg.cn/5caf2d895e41482ab69e909f8a0c8353.gif#pic_center)

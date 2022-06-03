# -*- coding: utf-8 -*-
# Author Frank Hu
# GitBook auto summary
# summary all .md files in a GitBook folder

import argparse
import os
import re

ignore_list = ['_book', 'node_modules', 'img']

def output_markdown(dire, base_dir, output_file, append, iter_depth=0):
    """Main iterator for get information from every file/folder

    i: directory, base directory(to calulate relative path), 
       output file name, iter depth.
    p: Judge is directory or is file, then process .md/.markdown files.
    o: write .md information (with identation) to output_file.
    """
    top_list = os.listdir(dire)
    for i in top_list:
       if i in ignore_list:
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

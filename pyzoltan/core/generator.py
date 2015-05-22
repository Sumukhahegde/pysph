#!/usr/bin/env python
'''
Module to collect and generate source files from mako template files.

When used to locate source files as a main program:
    The template files must have an extension '.mako'.
    The generated files have the name same as the mako file but with the '.mako'
    removed.
    Example: `carray.pyx.mako` is generated into `carray.pyx`
'''

import glob
import os
import sys


def is_modified_later(filename1, filename2):
    '''Return `True` if the file1 is modified later than file2'''
    return os.stat(filename1).st_mtime > os.stat(filename2).st_mtime

def generate_files(dirname, if_modified=True):
    '''Generates source files from the template files with extension `.mako`

    If `if_modified` is True (default), the source file will be created only
    if the template has been modified later than the source
    '''
    for filename in glob.glob(os.path.join(dirname, '*.mako')):
        outfile = filename[:-5]
        message = 'generating file {outfile} from {filename}'.format(
            outfile=outfile, filename=filename
        )
        if if_modified and not is_modified_later(filename, outfile):
            print('not ' + message)
        else:
            from mako.template import Template
            print(message)
            template = Template(filename=filename)
            with open(outfile, 'w') as fp:
                fp.write(template.render())

def main(paths=None):
    '''Generates source files using mako template files.

    Parameters
    -----------

    - paths:  is a list of directories to convert.  If None, all files in
      current file's directory are converted.

    '''
    if not paths:
        generate_files(os.path.dirname(__file__))
    else:
        for pth in paths:
            generate_files(pth)

if __name__ == '__main__':
    import sys
    if '--help' in sys.argv or '-h' in sys.argv:
        print 'usage:'
        print '    generator.py [filenames]'
        print
        print('    Convert template files with extension .mako into '
               'source files')
        print ('    If filenames is omitted all .mako files in current '
        'directory will be converted')

    else:
        main(sys.argv[1:])


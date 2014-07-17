
PyMakeMeLazyNDumb
-----------------

Good computer users and programmers are lazy and dumb. Lazy because they believe in automation as repeatable is boring for them and dumb because they are not ever satisfied with what others try to tell them. The aim of PyMakeMeLazyNDumb is to provide all these lazy and dumb people a simple but super automation tool through which they become more lazy. This tool shall do the following :

    * create good directories hierarchies,
    * create various kind of files with information headers,
    * launch their favorite applications instances at startup or any time,
    * download/install/build softwares required,
    * manage/compile/build/document source codes,
    * uploads/downloads multiple files to and from remote machines,
    * control remote machines with various commands,

and blah blah ...     

The PyMakeMeLazyNDumb tool is a container for these python apps and the release pattern shall be in form of the release of few of these python apps at a time. The v0.0.6 features the following python scripts/modules/apps :

[pygenericroutines.py] is a generic python module that comprises of several general purpose routines required most of the times by python automation tools. All the components of PyMakeMeLazyNDumb are based upon it heavily. The v0.0.6 of the module carries some new functionalities over the previous version.

[pycreateflswthdr.py] is a python app that creates various files having .c, .h, .cpp, .hpp, .java, .py, .pl, .rb, .lua, .php, .sh, .mak, .sql extensions with appropriate commented information headers. Some of the generic fields of the commented info headers are filled automatically. So use this simple but effective app next time when you want to generate files you or others could track later on. The v0.0.4 of the app carries some improvements over the previous version.

For example - if you want to generate example1.c, example2.py, example.sql files in your home directory then the command to type is :

    python pycreateflswthdr.py -d ~ example1.c example2.py example3.sql

If you want to append an info header to an already existing file then the command to type is :

    python pycreateflswthdr.py -a example4.mak

If you want to stuff Author, Download link & License entries (these are the common fields among generated multiple files) in the generated information header(s) as per your choice then create a text file config.conf in the current working directory with entries as shown below :

    # test config file for PyMakeMeLazyNDumb

    [pycreateflswthdr]

    Author        = Ankur Kumar Sharma
    Download link = http://richnusgeeks.wordpress.com
    License       = Public Domain

here pycreateflswthdr is the section name contained in the square brackets and Author, Download link & License are the entries for which you want to use
your values instead of the automatically generated values. For example - if you want to generate (for append use -a option as shown above) example5.lua, example6.cpp, example7.rb with values taken from config.conf then the command to type is :

    python pycreateflswthdr.py -c example5.lua example6.cpp example7.rb 
   
To see the usages of the app, the command is :

    python  pycreateflswthdr.py -h

The app backs up existing files both in creation and append modes with extension .bak.timestamp .This app logs all the warning and error messages in a log file named activity.log in the current working directory from where pycreateflswthdr.py is invoked. Once this log file is created, all the subsequent warnings and errors are appended to it. 

[pycreatemyspace.py] is a python app that creates an hierarchy of directories as per user provided arguments. A good directories hierarchy is the simplest way to effectively manage data so this app makes it easy to store and track your otherwise scattered data. You can mention the list of directories and subdirectories to be created on the command line itself or the app can read the list of the directories and subdirectories from a config file. You can also mention the destination directory where all these directories and subdirectories are created.
The v0.0.2 of the app carries an improvement over the previous version.

For example - if you want to create directories dir1, dir2, dir3 in the current location from where you run pycreatemyspace.py then the command to type is :

    python pycreatemyspace.py -p 'dir1 dir2 dir3'

If you also want to create some subdirectories in every created directory then the command to type is :

    python pycreatemyspace.py -p 'dir1 dir2 dir3' -s 'subdir1 subdir2 subdir3'

If you want to create your directories and subdirectories in your home directory then the command to type is :

    python pycreatemyspace.py -d ~ 'dir1 dir2 dir3' -s 'subdir1 subdir2 subdir3'

If you want the directories and subdirectories to be read from a configuration file then create a text file config.conf in the directory from where you run pycreatemyspace.py as shown below :

     #test config file for PyMakeMeLazyNDumb

    [pycreatemyspace]

    Directories = dir1 dir2 dir3
    Subdirectories = subdir1 subdir2 subdir3

now the command to type is :

    python pycreatemyspace.py -c

To see the usages of the app, the command is :

    python  pycreateflswthdr.py -h

The app only creates non existing directories and subdirectories from the listing provided so your existing directories and subdirectories are always safe even if you include those in the listings. This app logs all the warning and error messages in a log file named activity.log in the current working directory from where pycreatemyspace.py is invoked. Once this log file is created, all the subsequent warnings and errors are appended to it.
          

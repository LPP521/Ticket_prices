##python2.7, Unbuntu 14.04 LTS 64
---

##FIRST: gtk, webkit  
https://code.google.com/p/pywebkitgtk/
```
    Firstly grab the pywebkitgtk package from your distribution. If you want to build from source, follow the steps below.  

    Grab the source tarball at http://code.google.com/p/pywebkitgtk/downloads/list and extract it.  
    Build the library by following the command lines below:  
    $ ./configure --prefix=/pywebkitgtk/install/path  
    $ make  
    $ make install  
    That's it. As an extra step, you can try the demo browser by    following this step:
    
    $ python demos/tabbed_browser.py
    If you have installed pywebkitgtk in a non-standard location (i.    e. not in /usr or /usr/local), you might want to use the    following:
    
    $ PYTHONPATH=/pywebkitgtk/install/path python demos/browser.py
```
---
- `./configure`

 - error: could not find Python headers  
    `sudo apt-get install python-dev`

 - error: Package requirements (libxslt gthread-2.0 pygtk-2.0) were not met:  
      `sudo apt-get install python-gtk2-dev`  
      `sudo apt-get install libxslt1-dev`

 - No package 'webkit-1.0' found
    ```
    安装 libwebkitgrk-dev包
    1. sudo apt-get install aptitude
    2. sudo aptitude install libwebkitgtk-dev
    ```


##SECOND: beautifulsoup4  
  
 - `sudo pip install beautifulsoup4`
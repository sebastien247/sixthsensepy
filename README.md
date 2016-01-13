Syxthsense
=========


Dans le cadre d'un projet de fin d'année nous avons effectué le portage du projet [SixthSense](https://github.com/sixthsense/sixthsense/) créer par Pranav Mistry. Nous nous sommes basé sur le travail effectué sur ce [repository](https://github.com/chendaxixi/sixthSense_).

----------


Dépendances
----------------

* python 2.7
* wxPython (Phoenix)
* OpenCV 2
* ystockquote
* pywapi
* PyUserInput

### <i class="icon-cog"></i>Installation Ubuntu :

#### <i class="icon-file"></i> Installation de wxPython (Phoenix)

    sudo apt-get install dpkg-dev build-essential python2.7-dev libwebkitgtk-dev libjpeg-dev libtiff-dev libgtk2.0-dev libsdl1.2-dev libgstreamer-plugins-base0.10-dev libnotify-dev freeglut3 freeglut3-dev
    
    git clone https://github.com/wxWidgets/Phoenix
    
    cd Phoenix
    
    git submodule init
    git submodule update
    
    sudo python build.py dox etg --nodoc sip build
    sudo python build.py dox etg --nodoc sip install

##### Vérification :

    pip list
    python
    >>> import wx
    >>> wx.version()
    '3.0.3 gtk2 (phoenix)'

#### <i class="icon-file"></i> Installation de OpenCV

	sudo apt-get install python-opencv

#### <i class="icon-file"></i> Installation de pywapi

    sudo apt-get install python-pywapi

#### <i class="icon-file"></i> Installation de PyUserInput

	pip install python-xlib pyuserinput
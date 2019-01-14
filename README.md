## SuperX Application Store (AppStore)

The SuperX Application Store is the centralized package managment and application distribution channel for SuperX OS.

## Current state

    * Unreleased to public, planned release with SuperX 5.0 "Lamarr".
    * Debianization pending.

## Building

    * This section will be added once the project is Debianized.

## System Requirements

    * SuperX 5.0 "Lamarr" - Unreleased images available at cdn.superxos.com/iso
        OR
    * KDE Neon - neon.kde.org. Recommened to use SuperX as future compatibily with KDE Neon is uncertain.
    
## Install Dependencies
Install the following packages using apt (don't use pip etc.):

    * python3-pyqt5
    * python3-flask
    * appstream 
    * gir1.2-appstream-1.0
    * python3-aptdaemon
    * python3-apt
    
## Usage
    * Make superx-store executable: chmod +x ./superx-store
    * Run the superx-store: ./superx-store


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


## License
    Copyright (c) 2018-2019 Libresoft Technology Pvt. Ltd. and open source contributors.
    Entire list of contributors is mentioned below. 

Unless stated otherwise, all files in this project are licened under GNU [GPL 3.0](https://choosealicense.com/licenses/gpl-3.0/), including but not limited to the following files:

    * superx-store
    * superx_appstore_backend/appstore_backend.py
    
All files contained in parser_html/ directory are under [AGPL 3.0](https://choosealicense.com/licenses/agpl-3.0/), including but not limited to the following:
 
    * parser_html/appstore.py
    * parser_html/templates/appbar-btn-progstat.html  
    * parser_html/templates/app-bar.html  
    * parser_html/templates/appBox.html  
    * parser_html/templates/appDetails_carousel.html  
    * parser_html/templates/appdetails.html    
    * parser_html/templates/base.html  
    * parser_html/templates/categories.html  
    * parser_html/templates/category.html  
    * parser_html/templates/header.html  
    * parser_html/templates/index.html  
    * parser_html/templates/library.html  
    * parser_html/templates/list_package.html  
    * parser_html/templates/main.html  
    * parser_html/templates/redirect.html  
    * parser_html/templates/search.html  
    * parser_html/templates/task.html  
    * parser_html/templates/updates.html


## Contributors

This list names contributors whose submitted code/patches are merged into the main source code.<br>
You are free to add your name and at your choice, your email id once your code is merged with the<br>
main source code tree. 

    * Wrishiraj Kaushik <wrix@libresoft.in>
    * Deep Jyoti Choudhury
    * Varun Priolkar

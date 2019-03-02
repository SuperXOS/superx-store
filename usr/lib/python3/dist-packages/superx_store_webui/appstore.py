import os
from ast import literal_eval
from os import listdir
from os.path import isfile, join
from random import shuffle
from time import sleep
from pathlib import Path

from flask import Flask, render_template, request, send_from_directory

from superx_appstore_backend.appstore_backend import AppStoreBackend

_progress = None
app = Flask(__name__, static_url_path='/static')

backend_obj = AppStoreBackend()

tasks = []
current_task_details = None
current_progress = None
updates = None
installed = []
installedOthers = []
installedPreviously = []
complete_update = False
category_dict = {'Development': ['Building', 'Debugger', 'IDE', 'GUIDesigner', 'Profiling', 'RevisionControl', 'Translation', 'Database', 'ProjectManagement', 'WebDevelopment'],
                 'Office': ['Calendar', 'ContactManagement', 'Database', 'Dictionary', 'Chart', 'Email', 'Finance', 'FlowChart', 'PDA', 'ProjectManagement', 'Presentation', 'Spreadsheet', 'WordProcessor'],
                 'Graphics': ['2DGraphics', 'VectorGraphics', 'RasterGraphics', '3DGraphics', 'Scanning', 'OCR', 'Photography', 'Publishing', 'Viewer'],
                 'Utility': ['TextTools', 'TelephonyTools', 'Maps', 'Spirituality', 'Archiving', 'Compression', 'FileTools', 'Accessibility', 'Calculator', 'Clock', 'TextEditor'],
                 'Settings': ['DesktopSettings', 'HardwareSettings', 'Printing', 'PackageManager', 'Security', 'Accessibility'],
                 'Network': ['Dialup', 'InstantMessaging', 'Chat', 'IRCClient', 'Feed', 'FileTransfer', 'HamRadio', 'News', 'P2P', 'RemoteAccess', 'Telephony', 'VideoConference', 'WebBrowser', 'WebDevelopment', 'Monitor', 'Email'],
                 'Audio': ['HamRadio', 'Midi', 'Mixer', 'Sequencer', 'Tuner', 'AudioVideoEditing', 'Player', 'Recorder'],
                 'Video': ['TV', 'Player', 'Recorder'],
                 'AudioVideo': ['Database', 'Midi', 'Mixer', 'Sequencer', 'Tuner', 'TV', 'AudioVideoEditing', 'Player', 'Recorder', 'DiscBurning', 'Music', 'Audio', 'Video'],
                 'TextTools': ['Dictionary'],
                 'Game': ['ActionGame', 'AdventureGame', 'ArcadeGame', 'BoardGame', 'BlocksGame', 'CardGame', 'KidsGame', 'LogicGame', 'RolePlaying', 'Shooter', 'Simulation', 'SportsGame', 'StrategyGame', 'Emulator'],
                 'Education': ['Art', 'Construction', 'Music', 'Languages', 'ArtificialIntelligence', 'Astronomy', 'Biology', 'Chemistry', 'ComputerScience', 'DataVisualization', 'Economy', 'Electricity', 'Geography', 'Geology', 'Geoscience', 'History', 'Humanities', 'ImageProcessing', 'Literature', 'Maps', 'Math', 'NumericalAnalysis', 'MedicalSoftware', 'Physics', 'Robotics', 'Spirituality', 'Sports', 'ParallelComputing', 'Science'],
                 'Science': ['Art', 'Construction', 'Languages', 'ArtificialIntelligence', 'Astronomy', 'Biology', 'Chemistry', 'ComputerScience', 'DataVisualization', 'Economy', 'Electricity', 'Geography', 'Geology', 'Geoscience', 'History', 'Humanities', 'ImageProcessing', 'Literature', 'Maps', 'Math', 'NumericalAnalysis', 'MedicalSoftware', 'Physics', 'Robotics', 'Spirituality', 'Sports', 'ParallelComputing']}

@app.route('/')
def index():
    cwd = os.getcwd()

    image_path = '/usr/lib/python3/dist-packages/superx_store_webui/static/images/index/'
    image_list = [f for f in listdir(image_path) if
                    isfile(join(image_path, f))]
    
    top_app_id = ['org.gnome.Music.desktop', 'writetype.desktop', 'org.kde.kmouth', 'compton.desktop']
    top_app_list = []
    for app_id in top_app_id:
        top_app_list.append(backend_obj.appSummery(app_id))
    editor_app_id = ['gjackclock.desktop', 'kvirc.desktop', 'quake2-groundzero.desktop', 'geany.desktop']
    editor_app_list = []
    for app_id in editor_app_id:
        editor_app_list.append(backend_obj.appSummery(app_id))
    return render_template('index.html',
                           image_list=image_list,
                           top_app_list = top_app_list,
                           editor_app_list = editor_app_list
                           )


@app.route('/image/<path:filename>')
def display_file(filename):
    MEDIA_FOLDER = request.args.get('filepath')

    return send_from_directory(MEDIA_FOLDER, filename)


@app.route('/categories')
def categories():
    return render_template('categories.html')


@app.route('/category')
def category():
    category_list = []
    category = request.args.get('category')
    category_list.append(category)
    list_apps = backend_obj.listAppsInCategories(category_list)
    
    category_app_list = []
    for app_id in list_apps:
        category_app_list.append(backend_obj.appSummery(app_id))
    
    sub_category_list = category_dict[category]
    return render_template('category.html', category=category, app_list=category_app_list, sub_category_list = sub_category_list)

@app.route('/subcategory')
def subcategory():
    subcategory_list = []
    subcategory = request.args.get('subcategory')
    category = request.args.get('category')
    subcategory_list.append(subcategory)
    list_apps = backend_obj.listAppsInCategories(subcategory_list)
    
    subcategory_app_list = []
    for app_id in list_apps:
        subcategory_app_list.append(backend_obj.appSummery(app_id))
    
    sub_category_list = category_dict[category]
    return render_template('subcategory.html', subcategory=subcategory, app_list=subcategory_app_list, sub_category_list = sub_category_list)


@app.route('/update')
def update():
    updates = [{'name': 'python3-software-properties', 'security': True, 'section': 'admin', 'current_version': '5.0+superx17', 'candidate_version': '5.0+superx18', 'priority': 'optional'},
                {'name': 'iso-flag-png', 'security': Fasubcategorylse, 'section': 'universe/misc', 'current_version': '5.0+superx10', 'candidate_version': '5.0+superx11', 'priority': 'optional'}, {'name': 'superx-sources', 'security': False, 'section': 'admin', 'current_version': '5.0+superx17', 'candidate_version': '5.0+superx18', 'priority': 'optional'}, {'name': 'software-properties-common', 'security': False, 'section': 'admin', 'current_version': '5.0+superx17', 'candidate_version': '5.0+superx18', 'priority': 'optional'}]

    app_len = 0
    sec_len = 0
    for app in updates:
        if app['security'] == True:
            sec_len = sec_len + 1
        else:
            app_len = app_len + 1
    render_html = render_template('update.html',
                                  updates=updates,
                                  sec_len=sec_len,
                                  app_len=app_len
                                  )
    return render_html


@app.route('/details')
def detail():
    id = request.args.get('id')
    
    datas = backend_obj.appDetails(id)
    addons = []
    if datas['addons'] != None:
        for addon in datas['addons']:
            addons.append(backend_obj.appSummery(addon))
    
    if datas['description'] != None:
        last_four = datas['description'][-4:]
        
        old_string = datas['description']
        
        str_len = len(old_string)
        if str_len >= 500:
            #This part if to keep the 'show more' button in the same line
            if last_four == '/ul>':
                k = old_string.rfind("</li>")
                new_string = old_string[:k] + '<a data-toggle="collapse" data-target="#demo" onclick="myFunction()"\
                style="text-decoration:none; cursor:pointer"> &nbsp; &nbsp;Show Less</a>' + old_string[k:]
            elif last_four == '</p>':
                k = old_string.rfind("</p>")
                new_string = old_string[:k] + '<a data-toggle="collapse" data-target="#demo" onclick="myFunction()" \
                style="text-decoration:none; cursor:pointer"> &nbsp; &nbsp;Show Less</a>' + old_string[k:]
            #This part if to keep the 'show more' button in the same line END
        else:
            new_string = old_string
    elif datas['summery'] != None:
        new_string = "<p>" + datas['summery'] + "</p>"
    else:
        new_string = '<p>No Description</p>'
    
    categories_list = literal_eval(datas['categories'])
    app_id_list = backend_obj.listAppsInCategories(categories_list)
    shuffle(app_id_list)
    app_id_list = app_id_list[:4]
    
    related_app_list = []
    for app_id in app_id_list:
        if app_id != id:
            related_app_list.append(backend_obj.appSummery(app_id))
    
    ratings = {'avg_rating': '4.2', 'total_rating': '499', '5*': '70', '4*': '60', '3*': '50', '2*': '40', '1*': '30',
              'reviews': [
                          {'title': 'Lorem Ipsum is simply dummy text ', 'user': 'Lorem Ipsum', 'rating': '3', 'time': '1 year ago', 'review': "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book."},
                          
                          {'title': 'Lorem Ipsum is simply dummy text ', 'user': 'Lorem Ipsum', 'rating': '3', 'time': '2 year ago', 'review': "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book."}
                          ]
              } 
    return render_template('appdetails.html',
                           app=datas, addons=addons,
                           description = new_string,
                           app_list = related_app_list,
                           rating=3.1,
                           rating_comments=893,
                           category = categories_list,
                           current_task = current_task_details,
                           ratings=ratings,
                           )


@app.route('/uploadScreenshot/')
def uploadScreenshot():
    
    return render_template('redirect.html', redirect_url=request.referrer)

@app.route('/install/')
def installApp():
    return render_template('redirect.html', redirect_url=request.referrer)

@app.route('/remove/')
def removeApp():
    return render_template('redirect.html', redirect_url=request.referrer)

@app.route('/search')
def search():
    search_str = request.args.get('q')
    search_apps = backend_obj.searchApps(search_str)

    search_app_list = []
    for app_id in search_apps:
        search_app_list.append(backend_obj.appSummery(app_id))

    return render_template('search.html', app_list=search_app_list)


@app.route('/tasks/')
def task():
    print('tasks')
    print(task)
    print("current_task_details")
    print(current_task_details)
    return render_template('task.html', tasks=tasks,
                           current_task=current_task_details)


@app.route('/library/')
def library():
    return render_template('library.html',
                           installed=installed,
                           installedOthers=installedOthers,
                           installedPreviously=installedPreviously)


@app.route('/updates/')
def updates():
    return render_template('updates.html',
                           updates=updates)


@app.route('/login/')
def login():
    return render_template('login.html')

@app.context_processor
def context_processor():
    total_len = 0
    if isinstance(updates,(tuple,)):
        for update in updates:
            total_len = total_len + len(update)
        print(total_len)
        
    update_file = Path("/system-update")
    if update_file.is_file():
        file_exist = 1
    else:
        file_exist = 0
        
    if current_task_details == None:
        return dict(update_len=total_len, current_progress = current_progress, file_exist = file_exist, current_task_id = None)
    else:
        return dict(update_len=total_len, current_progress = current_progress, file_exist = file_exist, current_task_id = current_task_details['id'])


if __name__ == '__main__':
    sleep(.5)
    app.run(host='0.0.0.0', debug=True)

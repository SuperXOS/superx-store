from flask import Flask, render_template, request, send_from_directory
import os
from random import randint
from os import listdir
from os.path import isfile, join
from ast import  literal_eval
from superx_appstore_backend.appstore_backend import AppStoreBackend
from random import shuffle

_progress = None
app = Flask(__name__, static_url_path='/static')

backend_obj = AppStoreBackend()

tasks = []
current_task_details = None

@app.route('/')
def index():
    cwd = os.getcwd()

    image_path = os.path.join(cwd, 'parser_html/static/images/index')
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
    category = request.args.get('category')
    return render_template('category.html', category=category)


@app.route('/update')
def update():
    updates = [{'name': 'python3-software-properties', 'security': True, 'section': 'admin', 'current_version': '5.0+superx17', 'candidate_version': '5.0+superx18', 'priority': 'optional'},
                {'name': 'iso-flag-png', 'security': False, 'section': 'universe/misc', 'current_version': '5.0+superx10', 'candidate_version': '5.0+superx11', 'priority': 'optional'}, {'name': 'superx-sources', 'security': False, 'section': 'admin', 'current_version': '5.0+superx17', 'candidate_version': '5.0+superx18', 'priority': 'optional'}, {'name': 'software-properties-common', 'security': False, 'section': 'admin', 'current_version': '5.0+superx17', 'candidate_version': '5.0+superx18', 'priority': 'optional'}]

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
    
    print(related_app_list)
    return render_template('appdetails.html',
                           data=datas, addons = addons,
                           description = new_string,
                           app_list = related_app_list,
                           rating=3.1,
                           rating_comments=893,
                           category = categories_list,
                           current_task = current_task_details
                           )


def most_fequent_color(image):
    colour_tuple = [None, None, None]
    for channel in range(3):
        # Get data for one channel at a time
        pixels = image.getdata(band=channel)

        values = []
        for pixel in pixels:
            values.append(pixel)

        colour_tuple[channel] = round((sum(values) / len(values)) - 10)

    return '#%02x%02x%02x' % tuple(colour_tuple)


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
    task = tasks
    current_task_detail = current_task_details
    
    print(current_task_detail)
    return render_template('task.html', tasks=task, current_task = current_task_detail)


@app.route('/library/')
def library():
    return render_template('library.html',
                           installed = backend_obj.listInstalled())


@app.route('/updates/')
def updates():
    return render_template('updates.html',
                           updates = backend_obj.listUpdates())

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

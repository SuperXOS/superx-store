#!/usr/bin/python3

import os
from os import listdir
from os.path import isfile, join

from flask import Flask, render_template, request

app = Flask(__name__)


class Index:

    def index(self):
        cwd = os.getcwd()

        image_path = os.path.join(cwd, 'parser_html/static/images/')
        image_list = [f for f in listdir(image_path) if
                      isfile(join(image_path, f))]

        print(image_list)
        return render_template('index.html', image_list=image_list)


class Categories:
    def categories(self):
        return render_template('categories.html')


# @app.route("/category/", methods=['POST', 'GET'])
class Category:
    def category(self):
        category = request.args.get('category')
        return render_template('category.html', category=category)


class Update:
    def update(self):
        updates = [{'name': 'python3-software-properties', 'security': True,
                    'section': 'admin', 'current_version': '5.0+superx17',
                    'candidate_version': '5.0+superx18',
                    'priority': 'optional'},
                   {'name': 'iso-flag-png', 'security': False,
                    'section': 'universe/misc',
                    'current_version': '5.0+superx10',
                    'candidate_version': '5.0+superx11',
                    'priority': 'optional'},
                   {'name': 'superx-sources', 'security': False,
                    'section': 'admin', 'current_version': '5.0+superx17',
                    'candidate_version': '5.0+superx18',
                    'priority': 'optional'},
                   {'name': 'software-properties-common', 'security': False,
                    'section': 'admin', 'current_version': '5.0+superx17',
                    'candidate_version': '5.0+superx18',
                    'priority': 'optional'}]

        app_len = 0
        sec_len = 0
        for app in updates:
            if app['security'] == True:
                sec_len = sec_len + 1
            else:
                app_len = app_len + 1
        render_html = render_template('update.html', updates=updates,
                                      sec_len=sec_len, app_len=app_len)
        return render_html


index_obj = Index()
categories_obj = Categories()
category_obj = Category()
update_obj = Update()

app.add_url_rule('/', 'Index', lambda: index_obj.index())
app.add_url_rule('/categories', 'Categories',
                 lambda: categories_obj.categories())
app.add_url_rule('/category/', 'Category', lambda: category_obj.category())
app.add_url_rule('/updates/', 'Update', lambda: update_obj.update())

if __name__ == '__main__':
    app.run(host='0.0.0.0')

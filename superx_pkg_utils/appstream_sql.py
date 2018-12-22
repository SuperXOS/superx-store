#!/usr/bin/python3

import gi

gi.require_version("AppStream", "1.0")

from gi.repository import AppStream
import sqlite3 as db

db_conn = db.connect('appstream.sqlite')
db_cur = db_conn.cursor()
db_conn.execute(
    'CREATE TABLE IF NOT EXISTS AppInformation(id, apt_pkg, name, summery, description, catagories, keywords, icon, screenshots, thumbnails, license, developer, addons)')

pool = AppStream.Pool()
pool.load()

cpts = pool.get_components()

for i in cpts:
    id = i.props.id
    pkg = str(i.props.pkgnames)
    name = i.props.name
    summery = i.props.summary
    desc = i.props.description
    categories = str(i.get_categories())
    keywords = str(set(i.props.keywords + i.get_search_tokens()))
    icon = i.get_icon_by_size(128, 128)

    screenshots = list()
    thumbnails = list()

    license = i.props.project_license
    developer = i.props.developer_name
    addons = list()

    if icon == None:
        icon = 'generic_icon'
    else:
        icon = str(AppStream.Icon.get_filename(icon))

    for j in i.get_screenshots():
        for x in j.get_images():
            screenshot_url = x.get_url()
            if screenshot_url.endswith('_orig.png'):
                screenshots.append(screenshot_url)
            elif '_224x' in screenshot_url:
                thumbnails.append(screenshot_url)


    if len(screenshots) == 0:
        screenshots = 'generic_screenshot'
    else:
        screenshots = str(screenshots)

    if len(thumbnails) == 0:
        thumbnails = 'generic_thumbnail'
    else:
        thumbnails = str(thumbnails)

    for k in i.get_addons():
        addons.append(k.props.id)

    if len(addons) == 0:
        addons = 'no_addons'
    else:
        addons = str(addons)



    db_conn.execute(
        "INSERT INTO AppInformation(id, apt_pkg, name, summery, description, catagories, keywords, icon, screenshots, thumbnails, license, developer, addons) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (id, pkg, name, summery, desc, categories, keywords, icon, screenshots, thumbnails, license, developer, addons))

db_conn.commit()

print(db_conn.execute(
    "SELECT * FROM AppInformation WHERE id='org.kde.dolphin.desktop'").fetchall())

db_conn.close()

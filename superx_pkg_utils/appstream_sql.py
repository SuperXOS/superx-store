#!/usr/bin/python3

import gi

gi.require_version("AppStream", "1.0")

from gi.repository import AppStream
import sqlite3 as db

db_conn = db.connect('appstream.sqlite')
db_cur = db_conn.cursor()
db_conn.execute(
    'CREATE TABLE IF NOT EXISTS AppInformation(id, apt_pkg, name, summery, description, catagories, keywords, icon, screenshots, thumbnails, launchable, license, developer, addons, extends, suggested)')

pool = AppStream.Pool()
pool.load()

cpts = pool.get_components()

for i in cpts[10].get_launchables():
    print(i.get_entries())

for i in cpts:
    id = i.props.id
    pkg = str(i.props.pkgnames)
    name = i.props.name
    summery = i.props.summary
    desc = i.props.description
    categories = str(i.get_categories())
    keywords = str(set(i.props.keywords + i.get_search_tokens()))
    icon = i.get_icon_by_size(128, 128)
    screenshots = []
    try:
        launchable = str(i.get_launchable(
            AppStream.LaunchableKind.DESKTOP_ID).get_entries())
    except AttributeError:
        launchable = 'no_launchable'
    thumbnails = []
    license = i.props.project_license
    developer = i.props.developer_name
    addons = []
    extends = str(i.get_extends())
    suggested = []

    if icon == None:
        icon = 'generic_icon'
    else:
        icon = str(AppStream.Icon.get_filename(icon))

    for j in i.get_screenshots():
        for x in j.get_images():
            screenshot_url = x.get_url()
            if screenshot_url.endswith('_orig.png') or '752x' in screenshot_url:
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

    for l in i.get_addons():
        addons.append(l.props.id)

    if len(addons) == 0:
        addons = 'no_addons'
    else:
        addons = str(addons)

    for m in i.get_suggested():
        suggested.append(m.get_ids())

    if len(suggested) == 0:
        suggested = 'no_suggests'
    else:
        suggested = str(suggested)

    db_conn.execute(
        "INSERT INTO AppInformation(id, apt_pkg, name, summery, description, catagories, keywords, icon, screenshots, thumbnails, launchable, license, developer, addons, extends, suggested) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (id, pkg, name, summery, desc, categories, keywords, icon, screenshots,
         thumbnails, launchable, license, developer, addons, extends,
         suggested))

db_conn.commit()

print(db_conn.execute(
    "SELECT * FROM AppInformation WHERE id='org.kde.dolphin.desktop'").fetchall())

db_conn.close()

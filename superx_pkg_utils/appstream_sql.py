#!/usr/bin/python3

import gi

gi.require_version("AppStream", "1.0")

from gi.repository import AppStream

from sqlalchemy import create_engine
from sqlalchemy import Table, Column, String, MetaData


class AppDatabase:

    def __init__(self, engine_url):
        self.db_engine = create_engine(engine_url)

        pool = AppStream.Pool()
        pool.load()

        cpts = pool.get_components()

        self.appstream_data = []

        for i in cpts:
            component_data = {}
            component_data['id'] = i.props.id
            component_data['apt_pkg'] = str(i.props.pkgnames)
            component_data['name'] = i.props.name
            component_data['summery'] = i.props.summary
            component_data['description'] = i.props.description
            component_data['categories'] = str(i.get_categories())
            component_data['keywords'] = str(i.props.keywords)
            icon = i.get_icon_by_size(128, 128)

            try:
                component_data['launchable'] = str(i.get_launchable(
                    AppStream.LaunchableKind.DESKTOP_ID).get_entries())
            except AttributeError:
                component_data['launchable'] = 'no_launchable'

            component_data['license'] = i.props.project_license
            component_data['developer'] = i.props.developer_name
            component_data['search_tokens'] = str(list(i.get_search_tokens()))
            component_data['extends'] = str(i.get_extends())
            suggested = []

            if icon == None:
                component_data['icon'] = 'generic_icon'
            else:
                component_data['icon'] = str(AppStream.Icon.get_filename(icon))

            screenshots = []
            thumbnails = []
            for j in i.get_screenshots():
                for x in j.get_images():
                    screenshot_url = x.get_url()
                    if screenshot_url.endswith(
                            '_orig.png') or '752x' in screenshot_url:
                        screenshots.append(screenshot_url)
                    elif '_224x' in screenshot_url:
                        thumbnails.append(screenshot_url)

            if len(screenshots) == 0:
                component_data['screenshots'] = 'generic_screenshot'
            else:
                component_data['screenshots'] = str(screenshots)

            if len(thumbnails) == 0:
                component_data['thumbnails'] = 'generic_thumbnail'
            else:
                component_data['thumbnails'] = str(thumbnails)

            addons = []
            for l in i.get_addons():
                addons.append(l.props.id)

            if len(addons) == 0:
                component_data['addons'] = 'no_addons'
            else:
                component_data['addons'] = str(addons)

            for m in i.get_suggested():
                suggested.append(m.get_ids())

            if len(suggested) == 0:
                component_data['suggested'] = 'no_suggests'
            else:
                component_data['suggested'] = str(suggested)

            self.appstream_data.append(component_data)

        self.appstream_to_sql()

    def appstream_to_sql(self):
        metadata = MetaData()
        self.AppInformation = Table('AppInformation', metadata,
                                    Column('id', String, primary_key=True),
                                    Column('apt_pkg', String),
                                    Column('name', String),
                                    Column('summery', String),
                                    Column('description', String),
                                    Column('categories', String),
                                    Column('keywords', String),
                                    Column('icon', String),
                                    Column('screenshots', String),
                                    Column('thumbnails', String),
                                    Column('launchable', String),
                                    Column('license', String),
                                    Column('developer', String),
                                    Column('search_tokens', String),
                                    Column('addons', String),
                                    Column('extends', String),
                                    Column('suggested', String),
                                    )
        try:
            metadata.create_all(self.db_engine)

            conn = self.db_engine.connect()
            conn.execute(self.AppInformation.insert(), self.appstream_data)

        except Exception as e:
            print("Error occurred while converting AppStream data to SQL!")
            print(e)

    def appstream_data_all(self, table='', query=''):
        query = "SELECT * FROM '{}';".format(table)
        print(query)
        with self.db_engine.connect() as connection:
            try:
                result = connection.execute(query)
            except Exception as e:
                print(e)
            else:
                for row in result:
                    print(row)  # print(row[0], row[1], row[2])
                result.close()
        print("\n")


if __name__ == '__main__':
    AppDatabase(
        engine_url='sqlite:////home/wrix/Workspace/New_AppStore/superx_pkg_utils/appstream.sqlite')

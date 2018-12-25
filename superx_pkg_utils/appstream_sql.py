#!/usr/bin/python3

import gi

gi.require_version("AppStream", "1.0")

from gi.repository import AppStream

from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey


class AppDatabase:

    def fetch_apps_data(self):

        cpts = self.pool.get_components()

        appstream_data = []

        for i in cpts:
            component_data = {
                'id': i.props.id,
                'name': i.props.name,
                'summery': i.props.summary,
                'description': i.props.description,
                'categories': str(i.get_categories()),
                'keywords': str(i.props.keywords),
                'license': i.props.project_license,
                'developer': i.props.developer_name,
                'search_tokens': str(list(i.get_search_tokens())),
                'extends': str(i.get_extends())
            }

            # Get data of each

            try:
                component_data['launchable'] = str(i.get_launchable(
                    AppStream.LaunchableKind.DESKTOP_ID).get_entries())
            except AttributeError:
                component_data['launchable'] = None

            suggested = []

            icon = i.get_icon_by_size(128, 128)
            if icon == None:
                component_data['icon'] = None
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
                component_data['screenshots'] = None
            else:
                component_data['screenshots'] = str(screenshots)

            if len(thumbnails) == 0:
                component_data['thumbnails'] = None
            else:
                component_data['thumbnails'] = str(thumbnails)

            addons = []
            for l in i.get_addons():
                addons.append(l.props.id)

            if len(addons) == 0:
                component_data['addons'] = None
            else:
                component_data['addons'] = str(addons)

            for m in i.get_suggested():
                suggested.append(m.get_ids())

            if len(suggested) == 0:
                component_data['suggested'] = None
            else:
                component_data['suggested'] = str(suggested)

            appstream_data.append(component_data)

        return appstream_data

    def fetch_category_data(self):
        cpts_category = self.pool.search('maya')
        for ids in cpts_category:
            print(ids.props.id)

    def __init__(self, engine_url):

        self.db_engine = create_engine(engine_url)

        self.pool = AppStream.Pool()
        self.pool.load()
        self.fetch_category_data()

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
        # self.Categories = Table('Categories', metadata,
        #                         Column('id', String, primary_key=True),
        #                         Column('name', String),
        #                         Column('Summery', String),
        #                         Column('icon', String),
        #                         Column('children', String),
        #                         )
        # self.CategoryItems = Table('CategoryItems', metadata,
        #                     Column('id', Integer, primary_key=True),
        #                     Column('category_id', ForeignKey('Categories.id')),
        #                     Column('app_id', ForeignKey('AppInformation.id'))
        #                            )

        try:
            metadata.create_all(self.db_engine)

            conn = self.db_engine.connect()
            conn.execute(self.AppInformation.insert(), self.fetch_apps_data())

        except Exception as e:
            print("Error occurred while converting AppStream data to SQL!")
            print(e)




if __name__ == '__main__':
    AppDatabase(
        engine_url='sqlite:////home/wrix/Workspace/New_AppStore/superx_pkg_utils/appstream.sqlite')

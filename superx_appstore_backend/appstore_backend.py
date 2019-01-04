#!/usr/bin/python

import gi
gi.require_version("AppStream", "1.0")
from gi.repository import AppStream

class AppStoreBackend():

    def appDetails(self, id):
        cpt = self.pool.get_components_by_id(id)[0]

        component_data = {
            'id': cpt.props.id,
            'pkg': cpt.get_pkgnames(),
            'name': cpt.props.name,
            'summery': cpt.props.summary,
            'description': cpt.props.description,
            'categories': str(cpt.get_categories()),
            'license': cpt.props.project_license,
            'developer': cpt.props.developer_name,
            'homepage': cpt.get_url(AppStream.UrlKind.HOMEPAGE),
            'extends': str(cpt.get_extends())
        }

        try:
            component_data['launchable'] = str(cpt.get_launchable(
                AppStream.LaunchableKind.DESKTOP_ID).get_entries())
        except AttributeError:
            component_data['launchable'] = None

        suggested = []

        icon = cpt.get_icon_by_size(128, 128)
        if icon == None:
            component_data['icon'] = None
        else:
            component_data['icon'] = str(AppStream.Icon.get_filename(icon))

        screenshots = []
        thumbnails = []
        for j in cpt.get_screenshots():
            for x in j.get_images():
                screenshot_url = x.get_url()
                if screenshot_url.endswith('_orig.png'):
                    screenshots.append(screenshot_url)
                elif '_624x' in screenshot_url:
                    thumbnails.append(screenshot_url)

        if len(screenshots) == 0:
            component_data['screenshots'] = None
        else:
            component_data['screenshots'] = screenshots

        if len(thumbnails) == 0:
            component_data['thumbnails'] = None
        else:
            component_data['thumbnails'] = thumbnails

        addons = []
        for l in cpt.get_addons():
            addons.append(l.props.id)

        if len(addons) == 0:
            component_data['addons'] = None
        else:
            component_data['addons'] = addons

        for m in cpt.get_suggested():
            suggested.append(m.get_ids())

        if len(suggested) == 0:
            component_data['suggested'] = None
        else:
            component_data['suggested'] = suggested

        return component_data

    def appSummery(self, id):

        app = self.pool.get_components_by_id(id)[0]
        component_data = {
            'id': app.props.id,
            'pkg': app.get_pkgnames(),
            'name': app.props.name,
            'summery': app.props.summary
        }
        icon = app.get_icon_by_size(128, 128)
        if icon == None:
            component_data['icon'] = None
        else:
            component_data['icon'] = str(AppStream.Icon.get_filename(icon))

        return component_data

    def editorsPick(self):
        editors_pick_apps = []
        with open('editors-pick.list') as f:
            editors_pick_list = f.readlines()
        editors_pick_list = [x.strip() for x in editors_pick_list]
        for i in editors_pick_list:
            editors_pick_apps.append(self.appSummery(i))

        return editors_pick_apps

    def topRated(self):
        top_apps = []
        with open('top-rated.list') as f:
            top_list = f.readlines()
        top_list = [x.strip() for x in top_list]
        for i in top_list:
            top_apps.append(self.appSummery(i))

        return top_apps

    def listAppsInCategories(self, categories):
        """Example self.listAppsinCategories(["Development", Audio, ...])"""
        category_apps = []
        for i in self.pool.get_components():
            if not len(list(set(i.get_categories()) & set(categories))) == 0:
                category_apps.append(i.props.id)

        return category_apps

    def searchApps(self, term):
        result = []
        result_ = self.pool.search(term)
        for i in result_:
            result.append(i.props.id)

        return result
    
    #TODO: Think of a better way to get similar applications. Don't use this method yet.
    def getSuggested(self, categories, keywords):
        suggested_apps = []
        search = self.searchApps(keywords)
        apps_in_categories = self.listAppsInCategories(categories)
        suggested_apps = list(set(search) & set(apps_in_categories))
        
        return suggested_apps

    def __init__(self):
        self.pool = AppStream.Pool()
        self.pool.load()
        


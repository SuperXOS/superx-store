#!/usr/bin/python

import os
import sys
from operator import itemgetter

import apt
import apt_pkg
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
            'extends': str(cpt.get_extends()),
            'isInstalled': self.isInstalled(cpt.get_pkgname())
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
            'summery': app.props.summary,
            'isInstalled': self.isInstalled(app.get_pkgname())
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

    # More functionality will be added to this function in the future.
    # TODO: Add current version number and available version number
    def isInstalled(self, pkg):
        if len(self.transacted) != len(set(self.transacted)):
            # Refresh cache when duplicates are found.
            self.transacted = []
            self.apt_cache = apt.Cache()
        try:
             installed = self.apt_cache[pkg].is_installed
        except KeyError:
            return False

        if pkg in self.transacted and installed:
            return False
        elif pkg in self.transacted and not installed:
            return True
        else:
            return installed

    def listInstalled(self):
        installed_apps = []
        for cpt in self.pool.get_components():
            if self.isInstalled(cpt.get_pkgname()):
                installed_apps.append(self.appSummery(cpt.props.id))
        installed_apps = sorted(installed_apps, key=itemgetter('name'))
        return installed_apps

    def listUpdates(self):
        SYNAPTIC_PINFILE = "/var/lib/synaptic/preferences"
        DISTRO = 'bionic'

        def clean(cache, depcache):
            """ unmark (clean) all changes from the given depcache """
            # mvo: looping is too inefficient with the new auto-mark code
            # for pkg in cache.Packages:
            #    depcache.MarkKeep(pkg)
            depcache.init()

        def saveDistUpgrade(cache, depcache):
            """ this functions mimics a upgrade but will never remove anything """
            depcache.upgrade(True)
            if depcache.del_count > 0:
                clean(cache, depcache)
            depcache.upgrade()

        def isSecurityUpgrade(pkg, depcache):
            def isSecurityUpgrade_helper(ver):
                """ check if the given version is a security update (or masks one) """
                security_pockets = [("Ubuntu", "%s-security" % DISTRO),
                                    ("gNewSense", "%s-security" % DISTRO),
                                    ("Debian", "%s-updates" % DISTRO)]

                for (file, index) in ver.file_list:
                    for origin, archive in security_pockets:
                        if (
                                file.archive == archive and file.origin == origin):
                            return True
                return False

            inst_ver = pkg.current_ver
            cand_ver = depcache.get_candidate_ver(pkg)

            if isSecurityUpgrade_helper(cand_ver):
                return True

            # now check for security updates that are masked by a
            # canidate version from another repo (-proposed or -updates)
            for ver in pkg.version_list:
                if (inst_ver and
                        apt_pkg.version_compare(ver.ver_str,
                                                inst_ver.ver_str) <= 0):
                    # print "skipping '%s' " % ver.VerStr
                    continue
                if isSecurityUpgrade_helper(ver):
                    return True

            return False

        """
        Return a list of dict about package updates
        """
        pkgs = []

        apt_pkg.init()
        # force apt to build its caches in memory for now to make sure
        # that there is no race when the pkgcache file gets re-generated
        apt_pkg.config.set("Dir::Cache::pkgcache", "")

        try:
            cache = apt_pkg.Cache(apt.progress.base.OpProgress())
        except SystemError as e:
            sys.stderr.write("Error: Opening the cache (%s)" % e)
            sys.exit(-1)

        depcache = apt_pkg.DepCache(cache)
        # read the pin files
        depcache.read_pinfile()
        # read the synaptic pins too
        if os.path.exists(SYNAPTIC_PINFILE):
            depcache.read_pinfile(SYNAPTIC_PINFILE)
        # init the depcache
        depcache.init()

        try:
            saveDistUpgrade(cache, depcache)
        except SystemError as e:
            sys.stderr.write("Error: Marking the upgrade (%s)" % e)
            sys.exit(-1)

        # use assignment here since apt.Cache() doesn't provide a __exit__ method
        # on Ubuntu 12.04 it looks like
        # aptcache = apt.Cache()
        for pkg in cache.packages:
            if not (depcache.marked_install(
                    pkg) or depcache.marked_upgrade(pkg)):
                continue
            inst_ver = pkg.current_ver
            cand_ver = depcache.get_candidate_ver(pkg)
            if cand_ver == inst_ver:
                continue
            record = {"name": pkg.name,
                      "isSecurity": isSecurityUpgrade(pkg, depcache),
                      }
            pkgs.append(record)

        app_updates = []
        system_updates = []
        security_counter = 0
        for cpt in self.pool.get_components():
            for package in pkgs:
                if package['name'] == cpt.get_pkgname():
                    package_ = self.appSummery(cpt.props.id)
                    if package['isSecurity']:
                        security_counter = security_counter + 1
                    app_updates.append(package_)
        for pkg in pkgs:
            for i in app_updates:
                if not pkg['name'] in i['pkg']:
                    if pkg['isSecurity']:
                        security_counter = security_counter + 1
                    system_updates.append(pkg)
        app_updates = sorted(app_updates, key=itemgetter('name'))
        return app_updates, system_updates, security_counter





    def __init__(self):
        self.apt_cache = apt.Cache()
        self.pool = AppStream.Pool()
        self.pool.load()
        self.transacted = []
        


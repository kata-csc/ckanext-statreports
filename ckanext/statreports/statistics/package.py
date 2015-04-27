'''Report CKAN dataset (package) statistics'''

import sqlalchemy as sa

import ckan.model as model
import ckan.model.license as license

def _table(name):
    return sa.Table(name, model.meta.metadata, autoload=True)


class PackageStats(object):
    '''
    Queries to gain package data
    '''

    @classmethod
    def total_packages(cls):
        '''
        Return total of packages
        Assuming state="active", type="dataset"

        :return: count
        '''
        res = model.Session.query(model.Package.id).filter(model.Package.state == "active").\
            filter(model.Package.type == "dataset").count()
        return res

    @classmethod
    def private_package_count(cls):
        '''
        Return total of unpublished packages
        Assuming state="active", type="dataset", private=True

        :return: count
        '''
        res = model.Session.query(model.Package.id).filter(model.Package.state == "active").\
            filter(model.Package.type == "dataset").filter(model.Package.private == True).count()
        return res

    @classmethod
    def public_package_count(cls):
        '''
        Return total of published packages
        Assuming state="active", type="dataset", private=False

        :return: count
        '''
        res = model.Session.query(model.Package.id).filter(model.Package.state == "active").\
            filter(model.Package.type == "dataset").filter(model.Package.private == False).count()
        return res

    @classmethod
    def license_type_package_count(cls):
        open_licenses = []
        conditional_licenses = []
        closed_licenses = []
        register = license.LicenseRegister()

        for unsorted in register.items():
            if unsorted[1].isopen():
                open_licenses.append(unsorted[0])
            else:
                closed_licenses.append(unsorted[0])

        open_license_count = model.Session.query(model.Package.id).filter(model.Package.state == "active").\
            filter(model.Package.type == "dataset").filter(model.Package.license_id.in_(open_licenses)).count()
        closed_license_count = model.Session.query(model.Package.id).filter(model.Package.state == "active").\
            filter(model.Package.type == "dataset").filter(model.Package.license_id.in_(closed_licenses)).count()

        return {'open': open_license_count, 'conditionally_open': 0, 'closed': closed_license_count}

    @classmethod
    def rems_package_count(cls):
        #TODO implement
        pass
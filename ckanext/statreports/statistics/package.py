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

        open_licenses = ['CC0-1.0', 'ODC-PDDL-1.0']
        conditional_licenses = ['ODbL-1.0', 'ODC-BY-1.0',
                                'CC-BY-1.0', 'CC-BY-ND-1.0', 'CC-BY-NC-SA-1.0', 'CC-BY-SA-1.0', 'CC-BY-NC-1.0', 'CC-BY-NC-ND-1.0',
                                'CC-BY-2.0', 'CC-BY-ND-2.0', 'CC-BY-NC-SA-2.0', 'CC-BY-SA-2.0', 'CC-BY-NC-2.0', 'CC-BY-NC-ND-2.0',
                                'CC-BY-3.0', 'CC-BY-ND-3.0', 'CC-BY-NC-SA-3.0', 'CC-BY-SA-3.0', 'CC-BY-NC-3.0', 'CC-BY-NC-ND-3.0',
                                'CC-BY-4.0', 'CC-BY-ND-4.0', 'CC-BY-NC-SA-4.0', 'CC-BY-SA-4.0', 'CC-BY-NC-4.0', 'CC-BY-NC-ND-4.0']
        not_closed_licenses = open_licenses + conditional_licenses

        open_license_count = model.Session.query(model.Package.id).filter(model.Package.state == "active").\
            filter(model.Package.type == "dataset").filter(model.Package.license_id.in_(open_licenses)).count()
        conditional_license_count = model.Session.query(model.Package.id).filter(model.Package.state == "active").\
            filter(model.Package.type == "dataset").filter(model.Package.license_id.in_(conditional_licenses)).count()
        closed_license_count = model.Session.query(model.Package.id).filter(model.Package.state == "active").\
            filter(model.Package.type == "dataset").filter(~model.Package.license_id.in_(not_closed_licenses)).count()

        return {'open': open_license_count, 'conditionally_open': conditional_license_count, 'closed': closed_license_count}

    @classmethod
    def rems_package_count(cls):
        #TODO implement
        pass
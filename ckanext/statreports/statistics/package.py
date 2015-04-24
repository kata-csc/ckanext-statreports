'''Report CKAN dataset (package) statistics'''

import sqlalchemy as sa

import ckan.model as model


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

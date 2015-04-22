__author__ = 'salum'

import sys
import logging

import sqlalchemy as sa

import ckan.model as model
from ckan.lib.cli import CkanCommand

log = logging.getLogger(__name__)

class Reporter(CkanCommand):
    '''
    Reporter is used to generate reports of ckan usage satistics

    '''
    summary = __doc__.split('\n')[0]
    usage = __doc__
    max_args = 1
    min_args = 0

    def command(self):
        self._load_config()


        if len(self.args) == 0:
            self.parser.print_usage()
            sys.exit(1)
        cmd = self.args[0]
        if cmd == 'users':
            self.count_users()

    def count_users(self):
        users = self.total_users()
        print(users)
        return users


    def total_users(self):
        '''
        Return total of users

        :return: count
        '''
        res = model.Session.query(model.User.id).count()
        return res




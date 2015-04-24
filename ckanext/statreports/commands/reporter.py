import sys
import logging

from ckan.lib.cli import CkanCommand
import ckan.model

from ckanext.statreports.statistics.user import UserStats

log = logging.getLogger(__name__)


class Reporter(CkanCommand):
    '''
    Generate reports of CKAN usage statistics

    Usage:
        reporter mail
            - Send an e-mail report to the address given in configuration
        reporter users
            - Show user count
        reporter visitors
            - Show count of unique portal visitors
        reporter visitors_logged
            - Show count of unique portal visitors for logged in users


    '''
    summary = __doc__.split('\n')[0]
    usage = __doc__
    max_args = 10
    min_args = 0

    def command(self):
        self._load_config()
        engine = ckan.model.meta.engine

        if len(self.args) == 0:
            self.parser.print_usage()
            sys.exit(1)

        cmd = self.args[0]

        if cmd == 'mail':
            raise Exception('Not implemented')  # TODO

        if cmd == 'users':
            print UserStats.total_users()

        if cmd == 'visitors':
            print UserStats.total_visitors(engine)

        if cmd == 'visitors_logged':
            print UserStats.total_logged_in(engine)


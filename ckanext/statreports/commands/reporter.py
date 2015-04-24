import sys
import logging

from ckan.lib.cli import CkanCommand

from ckanext.statreports.statistics.user import UserStats

log = logging.getLogger(__name__)


class Reporter(CkanCommand):
    '''
    Reporter is used to generate reports of CKAN usage statistics

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
            count = UserStats.total_users()
            print count







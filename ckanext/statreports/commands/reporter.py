import sys
import logging

from ckan.lib.cli import CkanCommand

from ckanext.statreports.statistics.user import UserStats

log = logging.getLogger(__name__)


class Reporter(CkanCommand):
    '''
    Generate reports of CKAN usage statistics

    Usage:
      reporter users
        - Show user count

    '''
    summary = __doc__.split('\n')[0]
    usage = '\n'.join(__doc__.split('\n')[1:])
    max_args = 10
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







from datetime import datetime
import pprint
import sys
import logging

from ckan.lib.cli import CkanCommand
import ckan.model

from ckanext.statreports.statistics.user import UserStats
from ckanext.statreports.statistics.package import PackageStats

log = logging.getLogger(__name__)


class Reporter(CkanCommand):
    '''
    Generate reports of CKAN usage statistics

    Usage:
        reporter new_users
            - Show monthly new users
        reporter mail_report
            - Send a usage report e-mail to the address given in configuration
        reporter report
            - Print usage report
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

    def _help(self):
        self.parser.print_usage()
        sys.exit(1)

    def _error(self, msg):
        print 'ERROR: %s' % msg
        exit()

    def _generate_report(self):
        message = u'''
CKAN usage report
-----------------

    Totals:
    -------
    Datasets: {datasets}
    Users: {users}
    Unique visitors: {visitors}
    Unique logged in users: {visitors_logged}

    '''.format(users=UserStats.total_users(),
               visitors=UserStats.total_visitors(self.engine),
               visitors_logged=UserStats.total_logged_in(self.engine),
               datasets=PackageStats.total_packages())

        monthly_new_users = UserStats.users_by_month()

        for i in range(0, 3):
            curdate = datetime.utcnow()
            month = (int(curdate.month) - i) % 12  # [0..11]
            year_month = '%s-%02d' % (curdate.year, 12 if month == 0 else month)
            message += u'''
    Month {month}:
    --------------
    Unique visitors: {visitors}
    Unique logged in users: {visitors_logged}
    New users: {new_users}
    '''.format(month=year_month,
               visitors=UserStats.total_visitors(self.engine, year_month=year_month),
               visitors_logged=UserStats.total_logged_in(self.engine, year_month=year_month),
               new_users=monthly_new_users.get(year_month, 0))

        return message

    def command(self):
        self._load_config()
        self.engine = ckan.model.meta.engine

        if len(self.args) == 0:
            self._help()

        cmd = self.args[0]

        if cmd == 'mail_report':
            config = self._get_config()
            try:
                mail_to = config['statreports.report_email']
            except KeyError:
                self._error('Please set up statreports.report_email in configuration under [app:main]')

            mailer_url = config.get('ckan.site_url', '')
            mail_body = self._generate_report()

            from ckan.lib.mailer import _mail_recipient  # Must by imported after translator object is initialized

            _mail_recipient('Recipient', mail_to, 'CKAN reporter', mailer_url, 'CKAN usage report', mail_body)

        elif cmd == 'report':
            print self._generate_report()

        elif cmd == 'users':
            print UserStats.total_users()

        elif cmd == 'new_users':
            monthly = UserStats.users_by_month()
            for month, users in monthly.iteritems():
                print '%s: %s' % (month, users)

        elif cmd == 'visitors':
            print UserStats.total_visitors(self.engine)

        elif cmd == 'visitors_logged':
            print UserStats.total_logged_in(self.engine)

        else:
            self._help()

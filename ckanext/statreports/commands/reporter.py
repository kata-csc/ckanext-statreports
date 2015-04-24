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
        reporter send_mail
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

    def _help(self):
        self.parser.print_usage()
        sys.exit(1)

    def _error(self, msg):
        print 'ERROR: %s' %s

    def command(self):
        self._load_config()
        engine = ckan.model.meta.engine

        if len(self.args) == 0:
            self._help()

        cmd = self.args[0]

        if cmd == 'send_mail':
            config = self._get_config()
            try:
                mail_to = config['statreports.report_email']
            except KeyError:
                self._error('Please set up statreports.report_email in configuration under [app:main]')

            mail_from = config.get('ckan.site_url', '')
            # mail_from = config.get('smtp.mail_from', '')
            message = u'''
    CKAN usage report
    -----------------

    Totals:
    -------
    Users: {users}
    Unique visitors: {visitors}
    Unique logged in users: {visitors_logged}
            '''

            mail_body = message.format(users=UserStats.total_users(),
                                       visitors=UserStats.total_visitors(engine),
                                       visitors_logged=UserStats.total_logged_in(engine))

            from ckan.lib.mailer import _mail_recipient  # Must imported after translator object is initialized

            _mail_recipient('Recipient', mail_to, 'CKAN reporter', mail_from, 'CKAN usage report', mail_body)

        elif cmd == 'users':
            print UserStats.total_users()

        elif cmd == 'visitors':
            print UserStats.total_visitors(engine)

        elif cmd == 'visitors_logged':
            print UserStats.total_logged_in(engine)

        else:
            self._help()

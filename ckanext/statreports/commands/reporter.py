'''Report CKAN usage statistics'''

from datetime import datetime
import sys
import logging
from dateutil.relativedelta import relativedelta

from ckan.lib.cli import CkanCommand
import ckan.model

from ckanext.statreports.statistics.user import UserStats
from ckanext.statreports.statistics.package import PackageStats

from ckanext.statreports import email_template

log = logging.getLogger(__name__)


# TODO: Tests. Maybe should be tested without ckanext-kata.

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
        reporter private_packages
            - Show number of private packages
        reporter public_packages
            - Show number of public packages
        reporter package_license_types
            - Show number of packages by license type (open, closed or conditionally open)
        reporter rems
            - Show number of packages using REMS service provided by CSC
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

        config = self._get_config()
        title = config.get('ckan.site_title', 'CKAN')
        machine = config.get('ckan.site_url', '')

        packages = PackageStats.license_type_package_count()

        message = email_template.header.format(title=title, machine=machine)
        message += email_template.totals.format(users=UserStats.total_users(),
                                                visitors=UserStats.total_visitors(self.engine),
                                                visitors_logged=UserStats.total_logged_in(),
                                                datasets=PackageStats.total_packages(),
                                                public=PackageStats.public_package_count(),
                                                private=PackageStats.private_package_count(),
                                                open_datasets=packages['free'],
                                                conditionally_open_datasets=packages['conditional'],
                                                closed_datasets=packages['other'],
                                                rems_datasets=PackageStats.rems_package_count(),
                                                )

        monthly_new_users = UserStats.users_by_month()

        for i in range(0, 5):
            curdate = datetime.utcnow()
            year_month = (curdate + relativedelta(months=-i)).isoformat()[:7]
            message += email_template.monthly.format(
                month=year_month if year_month != curdate.isoformat()[:7] else year_month + ' (incomplete)',
                visitors=UserStats.total_visitors(self.engine, year_month=year_month),
                visitors_logged=UserStats.total_logged_in(year_month=year_month),
                new_users=monthly_new_users.get(year_month, 0),
            )
        _monthly_packages = PackageStats.total_new_packages(6)
        _monthly_public = PackageStats.public_packages_monthly(6)
        _monthly_private = PackageStats.private_packages_monthly(6)
        _monthly_open = PackageStats.license_type_package_count_monthly(6).get('free')
        _monthly_conditional = PackageStats.license_type_package_count_monthly(6).get('conditional')
        _monthly_closed = PackageStats.license_type_package_count_monthly(6).get('other')
        monthly_packages = ['{0}: {1}'.format(item[0], item[1]) for item in _monthly_packages]
        monthly_public = ['{0}: {1}'.format(item[0], item[1]) for item in _monthly_public]
        monthly_private = ['{0}: {1}'.format(item[0], item[1]) for item in _monthly_private]
        monthly_open = ['{0}: {1}'.format(item[0], item[1]) for item in _monthly_open]
        monthly_conditional = ['{0}: {1}'.format(item[0], item[1]) for item in _monthly_conditional]
        monthly_closed = ['{0}: {1}'.format(item[0], item[1]) for item in _monthly_closed]
        message += email_template.monthly_datasets.format(
            monthly_packages=". ".join(monthly_packages),
            monthly_public=". ".join(monthly_public),
            monthly_private=". ".join(monthly_private),
            monthly_open=". ".join(monthly_open),
            monthly_conditional=". ".join(monthly_conditional),
            monthly_closed=". ".join(monthly_closed)
        )

        message += email_template.footer

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

            _mail_recipient('recipient', mail_to, 'CKAN reporter', mailer_url, 'CKAN usage report', mail_body)

            print 'Sent usage report e-mail'

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
            print UserStats.total_logged_in()

        elif cmd == 'private_packages':
            print PackageStats.private_package_count()

        elif cmd == 'public_packages':
            print PackageStats.public_package_count()

        elif cmd == 'package_license_types':
            packages = PackageStats.license_type_package_count()
            text = 'Freely accessible datasets: ' + str(packages.get('free')) + \
                   '\nConditionally freely accessible datasets: ' + str(packages.get('conditional')) + \
                   '\nOther datasets: ' + str(packages.get('other')) + '\n'
            print text

        elif cmd == 'rems':
            print PackageStats.rems_package_count()

        else:
            self._help()

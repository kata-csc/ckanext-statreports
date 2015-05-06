from ckan.lib.base import BaseController, render
from ckanext.statreports.statistics.user import UserStats
from ckanext.statreports.statistics.package import PackageStats
from ckan.model.meta import engine

class StatisticsController(BaseController):
    '''
    StatisticsController renders a simple stat page
    which can be used to keep track on various Etsin
    statistics.
    '''

    def render_stats(self):
        '''
        Renders the stats page
        '''

        # Save the user stats in extra_vars variable, which is then passed on to the template
        extra_vars = {}

        extra_vars["total_users"] = UserStats.total_users()
        extra_vars["total_visitors"] = UserStats.total_visitors(engine)     # unique visitors
        extra_vars["total_logged_in"] = UserStats.total_logged_in(engine)
        extra_vars["total_packages"] = PackageStats.total_packages()

        packages_by_license_type = PackageStats.license_type_package_count()

        extra_vars["packages_free"] = packages_by_license_type["free"]
        extra_vars["packages_conditional"] = packages_by_license_type["conditional"]
        extra_vars["packages_other"] = packages_by_license_type["other"]

        return  render('statreports/stats.html', extra_vars=extra_vars)
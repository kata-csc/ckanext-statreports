import ckan.plugins as p
import ckan.plugins.toolkit as toolkit

class StatReports(p.SingletonPlugin):

    p.implements(p.IConfigurer, inherit=True)
    p.implements(p.IRoutes, inherit=True)

    def update_config(self, config):
        toolkit.add_template_directory(config, 'templates')
        toolkit.add_public_directory(config, 'public')


    def before_map(self, map):

        map.connect('statreports',
                    '/statistics',
                    controller='ckanext.statreports.controllers:StatisticsController',
                    action='render_stats')

        return map
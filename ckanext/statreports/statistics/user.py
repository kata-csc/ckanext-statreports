'''User statistics'''

import ckan.model as model

class UserStats(object):
    '''User statistics'''

    @staticmethod
    def total_users():
        '''
        Return total user count

        :return: count
        '''
        return model.Session.query(model.User.id).count()

    @staticmethod
    def total_visitors(engine, year_month=None):
        '''
        Return total unique visitor count

        :param engine:
        :return: visitor count
        '''
        if year_month:
            sql = '''SELECT count(DISTINCT user_key) FROM tracking_raw
                     WHERE to_char(access_timestamp, 'YYYY-MM') LIKE %(year_month)s'''
        else:
            sql = 'SELECT count(DISTINCT user_key) FROM tracking_raw'

        return engine.execute(sql, year_month=year_month).fetchone()[0]

    @staticmethod
    def total_logged_in(engine, year_month=None):
        '''
        Return total logged in visitor count

        :param engine:
        :return: logged in visitor count
        '''
        if year_month:
            sql = '''SELECT count(DISTINCT user_key) FROM tracking_raw WHERE url = '/user/logged_in' AND
                     to_char(access_timestamp, 'YYYY-MM') LIKE %(year_month)s'''
        else:
            sql = '''SELECT count(DISTINCT user_key) FROM tracking_raw WHERE url = '/user/logged_in' '''
        return engine.execute(sql, year_month=year_month).fetchone()[0]



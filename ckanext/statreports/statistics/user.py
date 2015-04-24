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
    def total_visitors(engine):
        '''
        Return total unique visitor count

        :param engine:
        :return: visitor count
        '''

        sql = '''
            SELECT count(DISTINCT user_key)
            FROM tracking_raw
        '''
        return engine.execute(sql).fetchone()[0]

    @staticmethod
    def total_logged_in(engine):
        '''
        Return total logged in visitor count

        :param engine:
        :return: logged in visitor count
        '''

        sql = '''
            SELECT count(DISTINCT user_key)
            FROM tracking_raw
            WHERE url = '/user/logged_in'
        '''
        return engine.execute(sql).fetchone()[0]



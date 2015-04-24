'''Report CKAN user statistics'''

import ckan.model as model

import sqlalchemy as sa


def _table(name):
    return sa.Table(name, model.meta.metadata, autoload=True)


class UserStats(object):
    '''User statistics'''

    @staticmethod
    def total_users():
        '''
        Return total user count

        :return: count
        '''
        return model.Session.query(model.User.id).count()

    @classmethod
    def users_by_month(cls):
        '''
        New users by month

        :return: count
        '''
        user = _table('user')
        q = sa.select([sa.func.count('id'), sa.extract('year', user.c.created),
                       sa.extract('month', user.c.created)],
                      from_obj=[user]).\
            group_by('anon_1', 'anon_2').\
            order_by('anon_1', 'anon_2')
        res = model.Session.execute(q).fetchall()
        ret = {}
        for count, anon_1, anon_2 in res:
            # key = unicode(int(anon_1)) + "/" + unicode(int(anon_2))
            key = '%s-%02d' % (int(anon_1), int(anon_2))
            ret[key] = int(count)

        return ret

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



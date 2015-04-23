import ckan.model as model

class UserStats:

    @staticmethod
    def total_users():
        '''
        Return total of users

        :return: count
        '''
        res = model.Session.query(model.User.id).count()

        return res

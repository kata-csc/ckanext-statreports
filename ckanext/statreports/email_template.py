'''E-mail report template'''

header = u'''
CKAN usage report
-----------------

'''
totals = u'''
    Totals:
    -------
    Datasets: {datasets}
    Public dataset: {public}
    Private datsets: {private}
    Users: {users}
    Unique visitors: {visitors}
    Unique logged in users: {visitors_logged}

    '''

monthly = u'''
    Month {month}:
    --------------
    Unique visitors: {visitors}
    Unique logged in users: {visitors_logged}
    New users: {new_users}
    '''

footer = u'''
    Unique visitor differentiation is based on IP address and HTTP request header fields determining user
    agent (browser), preferred language and content encoding.
    '''

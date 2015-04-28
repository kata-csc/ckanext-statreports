'''E-mail report template'''

header = u'''
{title} usage report
------------------

'''
totals = u'''
    Totals:
    -------
    Datasets: {datasets}
        -----
        Public datasets: {public}
        Private datasets: {private}

        Open datasets: {open_datasets}
        Conditionally open datasets: {conditionally_open_datasets}
        Closed datasets: {closed_datasets}

        Datasets using REMS: {rems_datasets}
        -----
    Registered users: {users}
    Unique visitors: {visitors}
    Unique logged in users: {visitors_logged}

    '''

monthly = u'''
    Month {month}:
    --------------
        Unique visitors: {visitors}
        Unique logged in users: {visitors_logged}
        New registered users: {new_users}
    '''

footer = u'''
-----------------
Unique visitor differentiation is based on IP address and HTTP request header fields determining user
agent (browser), preferred language and content encoding.
'''

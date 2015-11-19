'''E-mail report template'''

header = u'''
{title} usage report (from {machine})
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

monthly_datasets = u'''
    Datasets, monthly:
    ------------------
    Datasets: {monthly_packages}
    Public datasets: {monthly_public}
    Private datasets: {monthly_private}

    Open datasets: {monthly_open}
    Conditionally open datasets: {monthly_conditional}
    Closed datasets: {monthly_closed}

    '''


footer = u'''
-----------------
Unique visitor differentiation is based on IP address and HTTP request header fields determining user
agent (browser), preferred language and content encoding.
'''

'''Report CKAN dataset (package) statistics'''

import datetime
from dateutil.relativedelta import relativedelta

import sqlalchemy as sa

import ckan.model as model

FREE_LICENSES = ['CC0-1.0', 'ODC-PDDL-1.0']
CONDITIONAL_LICENSES = ['ODbL-1.0', 'ODC-BY-1.0',
                        'CC-BY-1.0', 'CC-BY-ND-1.0', 'CC-BY-NC-SA-1.0', 'CC-BY-SA-1.0', 'CC-BY-NC-1.0',
                        'CC-BY-NC-ND-1.0','CC-BY-2.0', 'CC-BY-ND-2.0', 'CC-BY-NC-SA-2.0', 'CC-BY-SA-2.0',
                        'CC-BY-NC-2.0', 'CC-BY-NC-ND-2.0', 'CC-BY-3.0', 'CC-BY-ND-3.0', 'CC-BY-NC-SA-3.0',
                        'CC-BY-SA-3.0', 'CC-BY-NC-3.0', 'CC-BY-NC-ND-3.0', 'CC-BY-4.0', 'CC-BY-ND-4.0',
                        'CC-BY-NC-SA-4.0', 'CC-BY-SA-4.0', 'CC-BY-NC-4.0', 'CC-BY-NC-ND-4.0']
OTHER_LICENSES = FREE_LICENSES + CONDITIONAL_LICENSES


def _table(name):
    return sa.Table(name, model.meta.metadata, autoload=True)


class PackageStats(object):
    '''
    Queries to gain package data
    '''

    @classmethod
    def get_date_months_ago(cls, months_ago=12):
        '''
        Return list of tuples of this and previous months

        :param months_ago: the amount of months from now, e.g. 1 is this month only
        :return: list of tuples (year, month)
        '''
        if not isinstance(months_ago, int):
            months_ago = 12
        # Because there is no point in 0:
        if months_ago == 0:
            months_ago = 1
        date_ = datetime.date.today()
        return [((date_+relativedelta(months=-i)).year, (date_+relativedelta(months=-i)).month) for
                i in range(0, months_ago)]

    @classmethod
    def _extract_monthly_results(cls, pkgs, months):
        '''
        Extract results, on monthly basis
        :param pkgs: result query (pkgid, min, year, month)
        :param months: for how many months. E.g. 1 is this month only, 2 is this month and last month
        :return: [('yyyy-mm', total),...]
        '''
        _months = cls.get_date_months_ago(months)
        res = list()
        for y, m in _months:
            res.append((str(y) + '-' + str(m), sum(pkg.year == y and pkg.month == m for pkg in pkgs)))
        return res

    @classmethod
    def total_packages(cls):
        '''
        Return total of packages
        Assuming state="active", type="dataset"

        :return: count
        '''
        res = model.Session.query(model.Package.id).filter(model.Package.state == "active").\
            filter(model.Package.type == "dataset").count()
        return res

    @classmethod
    def packages_by_license(cls, private=False, license=None):
        res = model.Session.query(model.Package.id).\
                   filter(model.Package.state=="active").\
                   filter(model.Package.type=="dataset").\
                   filter(model.Package.license_id.in_(license)).\
                   filter(model.Package.private==private).\
                   filter(model.Package.id==model.PackageExtra.package_id).\
                   all()
        return res

    @classmethod
    def _total_new_packages(cls):
        sel = sa.text("""
select pkgid, min, cast(extract(year from min) as int) as year, cast(extract(month from min) as int) as month
from (select package_revision.id as pkgid, min(revision.timestamp) as min
from package_revision
join revision on revision.id = package_revision.revision_id
join (select id from package where state='active' and type='dataset') as ptb on ptb.id = package_revision.id
group by package_revision.id
order by min(revision.timestamp)) as tbl;
""")
        return model.Session.execute(sel).fetchall()

    @classmethod
    def total_new_packages(cls, months=6):
        if not isinstance(months, int):
            months = 6
        pkgs = cls._total_new_packages()
        return cls._extract_monthly_results(pkgs, months)

    @classmethod
    def private_package_count(cls):
        '''
        Return total of unpublished packages
        Assuming state="active", type="dataset", private=True

        :return: count
        '''
        res = model.Session.query(model.Package.id).filter(model.Package.state == "active").\
            filter(model.Package.type == "dataset").filter(model.Package.private == True).count()
        return res

    @classmethod
    def _packages_monthly(cls, private=False):
        sel = sa.text("""
select pkgid, min, cast(extract(year from min) as int) as year, cast(extract(month from min) as int) as month from
(select package_revision.id as pkgid, min(revision.timestamp) as min from package_revision
join revision on revision.id = package_revision.revision_id
join (select id from package where private={p} and state='active' and type='dataset') as ptb
on ptb.id = package_revision.id group by package_revision.id order by min(revision.timestamp)) as tbl;
""".format(p=':private'))
        return model.Session.execute(sel, {"private": private}).fetchall()

    @classmethod
    def private_packages_monthly(cls, months=6):
        '''
        Extract sum of packages for each month

        :param months: int
        :return: list of tuples: ('yyyy-mm', amount)
        '''
        if not isinstance(months, int):
            months = 6

        pkgs = cls._packages_monthly(private=True)

        return cls._extract_monthly_results(pkgs, months)


    @classmethod
    def public_package_count(cls):
        '''
        Return total of published packages
        Assuming state="active", type="dataset", private=False

        :return: count
        '''
        res = model.Session.query(model.Package.id).filter(model.Package.state == "active").\
            filter(model.Package.type == "dataset").filter(model.Package.private == False).count()
        return res

    @classmethod
    def public_packages_monthly(cls, months=6):
        '''
        Extract sum of packages for each month

        :param months: int
        :return: list of tuples: ('yyyy-mm', amount)
        '''

        if not isinstance(months, int):
            months = 6
        pkgs = cls._packages_monthly(private=False)

        return cls._extract_monthly_results(pkgs, months)

    @classmethod
    def license_type_package_count(cls):

        open_license_count = model.Session.query(model.Package.id).filter(model.Package.state == "active").\
            filter(model.Package.type == "dataset").filter(model.Package.license_id.in_(FREE_LICENSES)).count()
        conditional_license_count = model.Session.query(model.Package.id).filter(model.Package.state == "active").\
            filter(model.Package.type == "dataset").filter(model.Package.license_id.in_(CONDITIONAL_LICENSES)).count()
        closed_license_count = model.Session.query(model.Package.id).filter(model.Package.state == "active").\
            filter(model.Package.type == "dataset").filter(~model.Package.license_id.in_(OTHER_LICENSES)).count()

        return {'free': open_license_count, 'conditional': conditional_license_count, 'other': closed_license_count}

    @classmethod
    def _packages_monthly_by_license(cls, licenses, not_=''):
        parameters = [('license_{i}'.format(i=i), l) for i, l in enumerate(licenses)]
        if not_ not in ['', 'not ']:
            not_ = ""
        params = dict()
        for item in parameters:
            params[item[0]] = item[1]
        sel = sa.text("""
select pkgid, min, cast(extract(year from min) as int) as year, cast(extract(month from min) as int) as month from
(select package_revision.id as pkgid, min(revision.timestamp) as min from package_revision
join revision on revision.id = package_revision.revision_id
join (select id from package where state='active' and type='dataset' and license_id {n}in ({l})) as ptb
on ptb.id = package_revision.id group by package_revision.id order by min(revision.timestamp)) as tbl;
""".format(n=not_, l=','.join(':'+item[0] for item in parameters)))
        return model.Session.execute(sel, params).fetchall()

    @classmethod
    def license_type_package_count_monthly(cls, months=6):
        if not isinstance(months, int):
            months = 6
        pkgs = cls._packages_monthly_by_license(FREE_LICENSES, '')
        free = cls._extract_monthly_results(pkgs, months)
        pkgs = cls._packages_monthly_by_license(CONDITIONAL_LICENSES, '')
        conditional = cls._extract_monthly_results(pkgs, months)
        pkgs = cls._packages_monthly_by_license(OTHER_LICENSES, 'not ')
        other = cls._extract_monthly_results(pkgs, months)
        return {'free': free, 'conditional': conditional, 'other': other}


    @classmethod
    def rems_package_count(cls):
        '''
        Return total of published packages using REMS service provided by CSC.
        Assuming state="active", type="dataset", private=False

        :return: count
        '''

        res = model.Session.query(model.Package.id).filter(model.Package.state == "active").\
            filter(model.Package.type == "dataset").filter(model.Package.private == False).\
            filter(sa.and_(model.PackageExtra.package_id == model.Package.id,
                           model.PackageExtra.key == 'availability',
                           model.PackageExtra.value == 'access_application'))

        try:
            res2 = model.Session.query(model.PackageExtra).filter(
                sa.and_(model.PackageExtra.package_id == res[0].id,
                        model.PackageExtra.key == 'access_application_URL',
                        model.PackageExtra.value.like('https://reetta.csc.fi%'))).count()
        except IndexError:
            return 0

        return res2

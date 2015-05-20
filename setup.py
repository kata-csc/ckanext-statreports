from setuptools import setup, find_packages

version = '0.0.1'

setup(
    name='ckanext-statreports',
    version=version,
    description="Generate reports based on ckan usage statistics",
    long_description="""
    """,
    classifiers=[],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='',
    author='CSC - IT Center for Science ltd.',
    author_email='servicedesk@csc.fi',
    url='',
    license='AGPL3',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=['ckanext', 'ckanext.statreports'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[  # -*- Extra requirements: -*-
        'python-dateutil == 1.5',
    ],
    package_data={
        'ckan': [
            'i18n/*/LC_MESSAGES/*.mo',
        ]
    },
    message_extractors={
        'ckanext': [
            ('**.py', 'python', None),  #
            ('statreports/templates/**.html', 'ckan', None),
            ('statreports/templates/statreports/**.html', 'ckan', None),
        ],
    },

    entry_points=
    """
    [ckan.plugins]
    # Add plugins here, eg
    statreports = ckanext.statreports.plugin:StatReports
    [paste.paster_command]
    reporter = ckanext.statreports.commands.reporter:Reporter
    """,
)

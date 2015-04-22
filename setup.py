from setuptools import setup, find_packages
import sys, os

version = '0.0'

setup(
    name='ckanext-statreports',
    version=version,
    description="Generate sreports based on ckan usage statistics",
    long_description="""\
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
    ],
    entry_points= \
        """
        [ckan.plugins]
	# Add plugins here, eg
	myplugin=ckanext.statreports:StatReports
		[paste.paster_command]
	reporter = ckanext.statreports.commands.reporter:Reporter
	""",
)

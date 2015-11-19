Generate reports based on CKAN usage statistics

Installation
============

You can install the extension with:

`pip install -e git://github.com/kata-csc/ckanext-statreports.git#egg=ckanext-statreports`

Enable with adding `statreports` to plugins in ini file.
To receive report emails, add `statreports.report_email = [YOUR_EMAIL_ADDRESS]` to ini file

Requirements
============

* tested on CKAN 2.4.1


Usage
=====

The following actions can be run with ``paster --plugin=ckanext-statreports reporter`` command:

* mail_report
  * reads email address from ini file's statreports.report_email
* report
* users
* new_users
* visitors
* visitors_logged
* private_packages
* public_packages
* package_license_types
* rems

Getting monthly dataset statistics is only available in the full report




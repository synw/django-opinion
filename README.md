# django-polls

[![Build status](https://travis-ci.org/byteweaver/django-polls.svg?branch=master)](https://travis-ci.org/byteweaver/django-polls)

A simple and reusable polls application for django.

## Key features

* basic poll handling (poll, choices, votes)
* easy to extend

## Installation

If you want to install the latest stable release from PyPi:

    $ pip install django-polls

If you want to install the latest development version from GitHub:

    $ pip install -e git://github.com/byteweaver/django-polls#egg=django-polls

Add `polls` to your `INSTALLED_APPS`:

    INSTALLED_APPS = (
        ...
        'polls',
        ...
    )

Hook this app into your ``urls.py``:

    urlpatterns = patterns('',
        ...
        url(r'^polls/', include('polls.urls', namespace='polls')),
        ...
    )

## Settings and options

To use the bootstrap templates set add the setting:

	POLLS_TEMPLATE_SET='bootstrap'
	
To use a custom permission check function in order to know if the user can vote use this setting:

	POLLS_CUSTOM_PERMS_MANAGER='app.module.function'

Provide the path to your own function for an extra permissions check. This functions take request as argument and is supposed to return `True` or `False`

Example:

settings.py

	POLLS_CUSTOM_PERMS_MANAGER='myapp.utils.profile_checker'

This way polls app will use the function named profile_checker located in myapp directory in the file utils.py to manage extra permissions check.

	def profile_checker(request, email_verification_required=True):
	    profile=request.user.profile
	    if email_verification_required:
	        if not profile.email_is_verified:
	            messages.warning(request, 'Your email must be verified to vote')
	            return False
	    return True
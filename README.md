#Django Opinion

Polls application for Django.

## Installation

- Clone the repository:

- Add `opinion` to your `INSTALLED_APPS`:

  ```python
INSTALLED_APPS = (
    ...
    'opinion',
    ...
)
  ```

- Hook this app into your ``urls.py``:

  ```python
urlpatterns = patterns('',
    ...
    url(r'^polls/', include('opinion.urls', namespace='opinion')),
    ...
)
  ```
  
## Settings and options

### Customize templates

To avoid using the default bootstrap templates set add the setting:

	POLLS_TEMPLATE_SET='my_set'

Then create a `templates/opinion/my_set` directory and start customizing the templates.

You can also just overide the templates in `templates/opinion` if you don't want to bother with some extra settings.

### Custom vote permission check

To use a custom permission check function in order to know if the user can vote use this setting:

	POLLS_CUSTOM_PERMS_MANAGER='app.module.function'

Provide the path to your own function for an extra permissions check. This function takes `request` as argument and is supposed to return `True` or `False`.

Example:

In `settings.py` :

	POLLS_CUSTOM_PERMS_MANAGER='myapp.utils.profile_checker'

This way polls app will use the function named profile_checker located in myapp directory in the file utils.py to manage extra permissions check.

  ```python
def profile_checker(request, email_verification_required=True):
    profile=request.user.profile
    if email_verification_required:
        if not profile.email_is_verified:
            messages.warning(request, 'Your email must be verified to vote')
            return False
    return True
  ```

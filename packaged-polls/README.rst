=====
Polls
=====

Web based polls with django.

Quick start
-----------

1. Add 'polls' to INSTALLED_APPS:
	INSTALLED_APPS = [
		...
		'polls',
	]

2. Include the polls URLconf in your project urls.py:
	path('polls/', include('polls.urls')),

3. Run ``python manage.py migrate`` to create the models from polls.

4. start the dev server and visit localhost:8000/admin to create a poll

5. Visit localhost:8000/polls to view polls.


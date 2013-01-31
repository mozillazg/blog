一个表中的多个字段同时将另一个表作为外键

Unhandled exception in thread started by <bound method Command.inner_run of <django.contrib.staticfi
les.management.commands.runserver.Command object at 0x0240BCB0>>
Traceback (most recent call last):
  File "C:\Python26\lib\site-packages\django\core\management\commands\runserver.py", line 91, in inn
er_run
    self.validate(display_num_errors=True)
  File "C:\Python26\lib\site-packages\django\core\management\base.py", line 270, in validate
    raise CommandError("One or more models did not validate:\n%s" % error_text)
django.core.management.base.CommandError: One or more models did not validate:
apps.notification: Accessor for field 'sender' clashes with related field 'User.notification_set'. A
dd a related_name argument to the definition for 'sender'.
apps.notification: Accessor for field 'receiver' clashes with related field 'User.notification_set'.
 Add a related_name argument to the definition for 'receiver'.
apps.topic: Accessor for field 'user' clashes with related field 'User.topic_set'. Add a related_nam
e argument to the definition for 'user'.
apps.topic: Accessor for field 'last_reply_by' clashes with related field 'User.topic_set'. Add a re
lated_name argument to the definition for 'last_reply_by'.


http://markmail.org/message/5565u2du37gh2wdc#query:django%20messages%20models%20foreignkey+page:1+mid:fhhb72tj72kku5fi+state:results

http://stackoverflow.com/questions/2408989/more-than-1-foreign-key

http://stackoverflow.com/questions/6664589/multiple-foreign-keys-for-one-relation-in-django

http://stackoverflow.com/questions/583327/django-model-with-2-foreign-keys-from-the-same-table

https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.ForeignKey.related_name

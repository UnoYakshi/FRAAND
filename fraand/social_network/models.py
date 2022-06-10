"""
TODO: Add description for models...

Futures:

=============
- Custom User model...
=============
class User(MyBaseModel, AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255)
    alias = models.CharField(max_length=255, unique=True)  # Alias = username + random_letter + random_three_digits...
    city = models.CharField(max_length=255)
    stats = gave_num, returned_num, gave_away_num


=============
- Models separation...
=============
Soon the number of models will be bigger. Probably, the separation onto a few applications will be needed, too.
"""


import datetime
from typing import Dict

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Deferrable, UniqueConstraint
from taggit.managers import TaggableManager
from taggit.models import GenericUUIDTaggedItemBase, TaggedItemBase

from fraand.core.models import MyBaseModel


class UUIDTaggedItem(GenericUUIDTaggedItemBase, TaggedItemBase):
    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

        # app_label = 'social_network'


class Item(MyBaseModel):
    """Items people can share with each other..."""

    class Meta:
        ordering = ['-created_at']
        app_label = 'social_network'

    name = models.CharField(max_length=255)
    description = models.TextField()

    # If the item should be browsable...
    public = models.BooleanField(default=True)

    rent = models.BooleanField(default=False)

    city = models.CharField(max_length=255, default='Innopolis, RU')

    # Access granted to specific users or groups...
    # access = ...

    owner_uid = models.ForeignKey(User, unique=False, on_delete=models.CASCADE, related_name='items')

    tags = TaggableManager(through=UUIDTaggedItem)

    def __str__(self):
        return self.name

    def get_contacts(self) -> Dict[str, str]:
        """
        Returns all the contacts for the Item card...

        A la:
        user = User.objects.get(pk=self.owner_uid)
        contacts = user.contacts.all()
        return contacts
        """
        return {'email': 'some_email@mail.inpls', 'Telegram': '@grociepo'}


class Image(models.Model):
    """

    FIXME: READ IT https://docs.djangoproject.com/en/4.0/topics/db/examples/many_to_one/ !

    """

    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images/')
    default = models.BooleanField(default=False)


class Deal(MyBaseModel):
    """An act of lending an item from one person to another..."""

    class DealStatus(models.IntegerChoices):
        INIT = (1, 'Initiated')
        PENDING = (2, 'Pending')
        BORROWED = (3, 'Borrowed')
        COMPLETED = (4, 'Completed')
        FAILED = (5, 'Failed')
        ERROR = (6, 'Error')

    from_user_uid = models.UUIDField()
    to_user_uid = models.UUIDField()
    item_uid = models.UUIDField()

    due_date = models.DateTimeField(default=datetime.datetime.now() + datetime.timedelta(days=14))
    status = models.IntegerField(choices=DealStatus.choices, default=DealStatus.INIT)

    class Meta:
        constraints = [
            UniqueConstraint(
                name='unique_deal',
                fields=['from_user_uid', 'to_user_uid', 'item_uid'],
                deferrable=Deferrable.DEFERRED,
            )
        ]
        # unique_together = (('from_user_uid', 'to_user_uid', 'item_uid'),)

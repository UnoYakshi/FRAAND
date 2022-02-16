import uuid

from django.db import models

from fraand.core.models import MyBaseModel


class Tag(MyBaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        return super(Tag, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'social_network'


class Item(MyBaseModel):
    """Items people can share..."""

    name = models.CharField(max_length=255)
    description = models.TextField()

    # If the item should be browsable...
    public = models.BooleanField(default=True)

    # Access granted to specific users or groups...
    # access = ...

    tags = models.ManyToManyField(Tag, related_name='products', blank=True)

    # Can work either automatically (with `slugify_function()` name) or with explicit assign...
    # Needs https://django-extensions.readthedocs.io/en/latest/field_extensions.html...
    # slug = models.SlugField(populate_from='name')  # slugify_function=slug_name)
    # def slug_name(self, content):
    #     return content.replace('_', '-').lower()
    # def slugify_function(self, content):
    #     return content.replace('_', '-').lower()

    class Meta:
        ordering = ['-created_at']
        app_label = 'social_network'

    def __str__(self):
        return self.name


class Image(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images/')
    default = models.BooleanField(default=False)

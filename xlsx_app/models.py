from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
import os
# from django.contrib.contenttypes.fields import GenericForeignKey
# from django.contrib.contenttypes.models import ContentType



# Create your models here.
class Workbook(models.Model):
	slug = models.SlugField(unique=True, max_length=100)
	workbook = models.FileField()

	def get_absolute_url(self):
		return reverse('main_home:download', kwargs={"slug": self.slug})

def create_slug(instance, new_slug=None):
	slug = slugify(instance.workbook.name) #slugifying the title
	if new_slug is not None:
		slug = new_slug
	qs = Workbook.objects.filter(slug=slug).order_by("-id")
	exists = qs.exists()
	if exists:
		new_slug = "%s-%s" %(slug, qs.first().id)
		return create_slug(instance, new_slug=new_slug)
	return slug

# signal receiver
def pre_save_post_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_slug(instance)


pre_save.connect(pre_save_post_receiver, sender=Workbook)
from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
import os


class PostManager(models.Manager):
	def active(self, *args, **kwargs):
		return super(PostManager, self).filter(draft=False).filter(publish__lte=timezone.now())

class Slide_Template(models.Model):
	template_name = models.CharField(default="Template", max_length = 100)
	template = models.FileField(default=0, blank=True)
	slug = models.SlugField(unique=True, max_length=1000)

	def __unicode__(self):
		return str(self.id)

class ReportOutlineFile(models.Model):
	slug = models.SlugField(unique=True, max_length=100)
	filename = models.CharField(max_length = 100)
	report_outline = models.FileField()
	template = models.ForeignKey(Slide_Template, blank=False, on_delete=models.CASCADE)

	def get_absolute_url(self):
		return reverse('txttoppt:download', kwargs={"slug": self.slug})

class ReportOutlineByEditor(models.Model):	
	slug = models.SlugField(unique=True, max_length=100)
	filename = models.CharField(max_length = 100)
	outline = models.TextField()
	template = models.ForeignKey(Slide_Template, blank=False, on_delete=models.CASCADE)

	def get_absolute_url(self):
		return reverse('txttoppt:download', kwargs={"slug": self.slug})

def create_slug(instance, new_slug=None):
	try:
		slug = slugify(instance.filename) #slugifying the title
	except:
		slug = slugify(instance.template_name)
	if new_slug is not None:
		slug = new_slug
	qs_1 = ReportOutlineFile.objects.filter(slug=slug).order_by("-id")
	qs_2 = ReportOutlineByEditor.objects.filter(slug=slug).order_by("-id")
	qs_3 = Slide_Template.objects.filter(slug=slug).order_by("-id")
	qs_1_exists = qs_1.exists()
	qs_2_exists = qs_2.exists()
	qs_3_exists = qs_3.exists()

	if qs_1_exists:
		new_slug = "%s-%s" %(slug, qs_1.first().id)
		return create_slug(instance, new_slug=new_slug)

	if qs_2_exists:
		new_slug = "%s-%s" %(slug, qs_2.first().id)
		return create_slug(instance, new_slug=new_slug)

	if qs_3_exists:
		new_slug = "%s-%s" %(slug, qs_3.first().id)
		return create_slug(instance, new_slug=new_slug)

	return slug

# signal receiver
def pre_save_post_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_slug(instance)
		

pre_save.connect(pre_save_post_receiver, sender=ReportOutlineFile)
pre_save.connect(pre_save_post_receiver, sender=ReportOutlineByEditor)
pre_save.connect(pre_save_post_receiver, sender=Slide_Template)
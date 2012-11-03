from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User
from tinymce import models as tinymce_models
from slugify import slugify
from tagging.fields import TagField
from tagging.models import Tag
from django.conf import settings
from django.utils.html import strip_tags
from urlparse import urlparse
# Create your models here.

if 'south' in settings.INSTALLED_APPS:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules( [], ["^tinymce\.models.\HTMLField"] )

class Category( MPTTModel ):
    title = models.CharField( max_length = 100 )
    parent = TreeForeignKey( 'self', null = True, blank = True, related_name = 'children' )
    order = models.IntegerField( default = 99, db_index = True )

    class MPTTMeta:
        order_insertion_by = ['title']

    def __unicode__( self ):
        return self.title

    def slug( self ):
        return slugify( self.title )

class Post( models.Model ):
    title = models.CharField( max_length = 200 )
    content = tinymce_models.HTMLField()
    category = models.ManyToManyField( Category )
    author = models.ForeignKey( User, related_name = "%(app_label)s_%(class)s_related" )
    date_add = models.DateTimeField( auto_now_add = True )
    date_edit = models.DateTimeField( auto_now = True )
    status = models.CharField( max_length = 15, choices = settings.STATUS_CHOICES, default = 'active', db_index = True )
    source = models.URLField( blank = True, null = True )
    tags = TagField()

    class Meta:
        ordering = ['pk']

    def __unicode__( self ):
        return self.title

    def slug( self ):
        return slugify( self.title )

    def snippet( self ):
        striped = strip_tags( self.content )

        ret = striped[:250]
        if len( striped ) > 250:
            ret + '...'

        return ret

    def hostname( self ):
        o = urlparse( self.source )
        return o.hostname

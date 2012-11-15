from django.db import models
from django.conf import settings
from django.utils.html import strip_tags


from mptt.models import MPTTModel, TreeForeignKey

from urlparse import urlparse


from common.models import CommonCategory, CommonPost

class BookmarksCategory( CommonCategory ):
    pass

class BookmarksPost( CommonPost ):
    category = models.ManyToManyField( BookmarksCategory )
    site = models.URLField( null = True )

    def hostname( self ):
        o = urlparse( self.site )
        return o.hostname

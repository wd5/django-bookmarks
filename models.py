from django.db import models
from django.conf import settings
from django.utils.html import strip_tags
from django.utils.translation import ugettext_lazy as _


from mptt.models import MPTTModel, TreeForeignKey

from urlparse import urlparse

from common.models import CommonCategory, CommonPost

class BookmarksCategory( CommonCategory ):
    pass

class BookmarksPost( CommonPost ):
    category = models.ManyToManyField( 
        BookmarksCategory,
        related_name = "%(app_label)s_%(class)s_related",
        verbose_name = _( 'category' )
    )
    site = models.URLField( 
        null = True,
        verbose_name = _( 'site' )
    )

    def hostname( self ):
        o = urlparse( self.site )
        return o.hostname

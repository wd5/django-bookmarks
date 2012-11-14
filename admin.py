from django.contrib import admin
#from mptt.admin import MPTTModelAdmin

from common.admin import CommonPostAdmin, CommonCategoryAdmin
from . models import BookmarksCategory, BookmarksPost

class CategoryAdmin( CommonCategoryAdmin ):
    pass

class PostAdmin( CommonPostAdmin ):
    pass

admin.site.register( BookmarksCategory, CategoryAdmin )
admin.site.register( BookmarksPost, PostAdmin )


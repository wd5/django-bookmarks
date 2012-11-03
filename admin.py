from django.contrib import admin
#from mptt.admin import MPTTModelAdmin

from common.admin import CommonPostAdmin, CommonCategooryAdmin
from . models import Category, Post

class CategoryAdmin( CommonCategooryAdmin ):
    pass

class PostAdmin( CommonPostAdmin ):
    pass

admin.site.register( Category, CategoryAdmin )
admin.site.register( Post, PostAdmin )

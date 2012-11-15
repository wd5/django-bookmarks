from django import forms

from django.contrib.admin.widgets import FilteredSelectMultiple

from common.forms import CommonPostEditForm
from . models import BookmarksPost, BookmarksCategory

class BookmarksEditForm( CommonPostEditForm ):
    category = forms.ModelMultipleChoiceField( 
        queryset = BookmarksCategory.objects.all(),
        required = False,
        widget = FilteredSelectMultiple( 
            'categories',
            False,
        )
    )

    class Meta( CommonPostEditForm.Meta ):
        model = BookmarksPost
        fields = ( 'title', 'content', 'category', 'site', 'tags', )

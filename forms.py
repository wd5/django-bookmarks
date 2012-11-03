from models import Post, Category
from django import forms
from django.forms import ModelForm
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.translation import ugettext_lazy as _

class BookmarksEditForm( ModelForm ):
    category = forms.ModelMultipleChoiceField( 
        queryset = Category.objects.all(),
        required = False,
        widget = FilteredSelectMultiple( 
            'categories',
            False,
        )
    )

    class Meta:
        model = Post
        exclude = ( 'status', 'author', )

    class Media:
        css = {
            'all':( 
                'admin/css/widgets.css',
                'admin/css/forms.css',
            ),
        }
        # Adding this javascript is crucial
        js = ( 
            '/admin/jsi18n/',
        )

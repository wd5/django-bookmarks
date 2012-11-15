from django.conf.urls import patterns, include, url

# (?P<year>\d{4})
urlpatterns = patterns( 'bookmarks',
    url( r'^add/$', 'views.add', name = 'bookmarks-add' ),
    url( r'^edit/(?P<id>\d+)$', 'views.edit', name = 'bookmarks-edit' ),
    url( r'^category-(?P<id>\d+)(?:\-(?P<slug>[\w\-]+))?', 'views.category', name = 'bookmarks-category' ),
    url( r'^post-(?P<id>\d+)(?:\-(?P<slug>[\w\-]+))?', 'views.post', name = 'bookmarks-post' ),
    url( r'^(?:/?page-(?P<page>\d+))?', 'views.home', name = 'bookmarks-home' ),
 )


# -*- coding: utf-8 -*-
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.translation import ugettext_lazy as _
from zokiguide.decorators import render_to
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from . models import BookmarksPost, BookmarksCategory
from . forms import BookmarksEditForm

def get_categories():
    return BookmarksCategory.objects.get_query_set()

def get_posts( category = None, page = None ):

    posts = BookmarksPost.objects.filter( status = 'active' )

    if category:
        posts = posts.filter( category = category )

    paginator = Paginator( posts, 7 )

    try:
        posts = paginator.page( page )
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page( 1 )
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page( paginator.num_pages )

    return posts

def home( request, page = None ):

    categories = get_categories()
    posts = get_posts( page = page )

    data = {
        'categories' : categories,
        'posts' : posts,
    }

    return render( request, 'bookmarks/home.html', data )

def category( request, id, slug = None, page = None ):

    id = int( id )

    try:
        category = BookmarksCategory.objects.get( pk = id )
    except BookmarksCategory.DoesNotExist:
        raise Http404

    if category.slug() != slug:
        return redirect( 'bookmarks-category', id = id, slug = category.slug(), permanent = True )

    posts = get_posts( category = category, page = page )
    categories = get_categories()

    data = {
        'category':category,
        'posts':posts,
        'categories':categories,
    }

    return render( request, 'bookmarks/home.html', data )

#@render_to( 'bookmarks/post.html' )
def post( request, id, slug = None ):
    id = int( id )

    try:
        post = BookmarksPost.objects.get( pk = id )
    except BookmarksPost.DoesNotExist:
        raise Http404

    if post.slug() != slug:
        return redirect( 'bookmarks-post', id = id, slug = post.slug(), permanent = True )

    data = {
        'post':post,
        'categories':BookmarksCategory.objects.all(),
    }

    return render( request, 'bookmarks/post.html', data )

@login_required
def edit( request, id ):
    id = int( id )

    try:
        post = BookmarksPost.objects.get( pk = id )
    except BookmarksPost.DoesNotExist:
        raise Http404

    if request.method == "POST":
        form = BookmarksEditForm( request.POST, instance = post )
        if form.is_valid:
            form.save()
            post.status = 'active'
            post.save()

            return redirect( 'bookmarks-post', id = id )
    else:
        form = BookmarksEditForm( instance = post )

    data = {
        'form':form
    }
    return render( request, 'bookmarks/edit.html', data )


@login_required
def add( request ):
    if request.session.get( 'bookmarks-draft-id', '' ) and int( request.session['bookmarks-draft-id'] ) > 0:
        return redirect( 'bookmarks-edit', id = request.session['bookmarks-draft-id'] )
    else:
        post = BookmarksPost( status = 'draft', author = User.objects.get( pk = request.user.id ) )
        post.save()
        request.session['bookmarks-draft-id'] = post.id
        return redirect( 'bookmarks-edit', id = post.id )

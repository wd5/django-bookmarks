# -*- coding: utf-8 -*-
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from zokiguide.decorators import render_to
from django.contrib.auth.models import User

from . models import Post, Category
from . forms import BookmarksEditForm
#from . import settings as zs_settings

@render_to( 'bookmarks/home.html' )
def home( request ):
	data = {}
	return data

# @render_to('bookmarks/home.html')
@login_required
def add( request ):
	if request.session.get( 'bookmarks-draft-id', '' ) and int( request.session['bookmarks-draft-id'] ) > 0:
		return redirect( 'bookmarks-edit', id = request.session['bookmarks-draft-id'] )
	else:
		post = Post( status = 'draft', author = User.objects.get( pk = request.user.id ) )
		post.save()
		request.session['bookmarks-draft-id'] = post.id
		return redirect( 'bookmarks-edit', id = post.id )

@render_to( 'bookmarks/category.html' )
def category( request, id, slug = None ):

	id = int( id )

	try:
		category = Category.objects.get( pk = id )
	except Category.DoesNotExist:
		raise Http404

	if category.slug() != slug:
		return redirect( 'bookmarks-category', id = id, slug = category.slug(), permanent = True )

	data = {
		'category':category,
		'posts':Post.objects.filter( category = id )[:10],
		'categories':Category.objects.all(),
	}

	return data

@render_to( 'bookmarks/post.html' )
def post( request, id, slug = None ):
	id = int( id )

	try:
		post = Post.objects.get( pk = id )
	except Post.DoesNotExist:
		raise Http404

	if post.slug() != slug:
		return redirect( 'bookmarks-post', id = id, slug = post.slug(), permanent = True )

	data = {
		'post':post,
		'categories':Category.objects.all(),
	}

	return data

@login_required
@render_to( 'bookmarks/edit.html' )
def edit( request, id ):
	id = int( id )

	try:
		post = Post.objects.get( pk = id )
	except Post.DoesNotExist:
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
	return data

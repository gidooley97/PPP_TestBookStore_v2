from django.shortcuts import render

from django.views import generic, View
from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from .search_checkmate import search
from lxml import etree
from django.db import models
from django.db.models import Q
from django.views.generic import TemplateView, ListView
from django.core.paginator import Paginator
from urllib.parse import urlencode
from django import template
from .models import Profile, Query_Manager
from django.contrib.auth.models import Group
from .serializers import SiteBookDataSerializer
from rest_framework.response import Response 
from rest_framework.views import APIView 
from django.contrib.auth.decorators import login_required
import datetime

#def index(request):
    #profiles = Profile.objects.all()
    #print(request)
    #return render(request, 'index.html', {'users': users})

def detail(request, book_id):
    try:
        book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        raise Http404("Question does not exist")

    return render(request, 'detail.html', {'book': book})


"""
This API calls the checkmate search module that uses the checkmate library to search for a given book.

Params:
    None
Return:
    JSON: serialized json of book matches.
"""
class SearchAPIView(APIView):
    
    print("SearchResultsView")
    
    def get(self,request): 
        book_matches = []#only a list of book matches no scores for now.
        print('request Meth:', request.method)
        query = self.request.GET
        title = query.get('title')
        print(title)
        authors = str(query.get('authors')).split(',')
        print(authors)
        isbn= query.get('isbn')
        print(isbn)
        book_url = query.get('book_url')
        print(book_url)
        if title is None:
            title="Lord" ##Change this value. if you want to search by a differnt book title.
        object_list=search(book_title=title, authors=authors,isbn_13=isbn,url=book_url)
        print(object_list)        
        serializer = SiteBookDataSerializer(object_list, many=True)
        return Response({"books":serializer.data})


@login_required(login_url='/accounts/login/')
def SearchView(request):
	return render(request, 'search.html')

@login_required(login_url='/accounts/login/')

def list_companies(request):
    group_list = Group.objects.all()
    return render(request, "company_list.html", {"group_list": group_list})

#def company_report(request): #no one will ever access these views
# We will ourselves ask therm to login and give them an option to logout 
 #   return render(request, "company_report.html")

# class LogoutView(TemplateView):
#     template_name = 'registration/logged_out.html'

# class LoginView(TemplateView):
#     template_name = 'registration/login.html'

class MyView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'


@login_required(login_url='/accounts/login/')
def activity(request):                    #This is the Report Page
    # group_list = Group.objects.all() #no need to get all groups
    user = request.user 
    #let's do something different for admin users
    group = user.groups.all()[0]
    if user == 'admin':
        #do something
        pass
    users_in_group = User.objects.filter(groups__name=group)
    #Take care of getting queries made
    return render(request, "activity.html", {"group": group, "user_list":users_in_group}) #connection with database



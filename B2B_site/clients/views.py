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

from .search_checkmate import search
from lxml import etree
from django.db import models
from django.db.models import Q
from django.views.generic import TemplateView, ListView
from django.core.paginator import Paginator
from urllib.parse import urlencode
from django import template
from .models import Profile, Query_Manager
from django.contrib.auth.models import Group,User
from .serializers import SiteBookDataSerializer
from rest_framework.response import Response 
from rest_framework.views import APIView 
from .forms  import EditForm
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
class SearchResultsView(APIView):
    
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


def SearchForm(request):
	#creating a new form
	form = SignupForm()

	return render(request, 'search.html', {'form':form})


def list_companies(request):
    group_list = Group.objects.all()
    return render(request, "company_list.html", {"group_list": group_list})

def company_edit_form(request,group_id):
    company = Group.objects.get(id = group_id)
    permissions = company.permissions.all()
    #------ Get Company Contact ----------
    all_users_in_group = User.objects.filter(groups__name = company.name)
    company_contact = all_users_in_group.filter(groups__name = 'Company Contact')
    cc_user = company_contact
    form = EditForm(initial = {'company_name': company.name, 'search_these' : permissions})

    if request.method == 'POST':
        form = EditForm(request.POST) # if post method then form will be validated
        if form.is_valid():
            clean_name = form.cleaned_data['company_name']
            company.name = clean_name
            clean_permissions = form.cleaned_data['search_these']
            company.permissions = clean_permissions
            company.save()
           
    if form.is_valid():
        return HttpResponse("valid")

    else:
        form = EditForm(initial = {'company_name': company.name})
    return render(request, "company_edit.html",{'form': form})



   # return render(request, "company_edit.html", {"group": group})





class logoutView(TemplateView):
    template_name = 'registration/logged_out.html'

class loginView(TemplateView):
    template_name = 'registration/login.html'



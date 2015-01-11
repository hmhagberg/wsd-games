from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http import Http404

# Create your views here.
def home (request):
	return render_to_response('games/index.html')
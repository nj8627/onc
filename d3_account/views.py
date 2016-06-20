from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from django.http import HttpResponse
from django.db.models import Sum
import time
from django.db.models import Q
from django.core.urlresolvers import reverse
import json
from django.core.serializers.json import DjangoJSONEncoder
import operator
from collections import OrderedDict
from django.db.models import Q
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    return render_to_response('index.html',{},context_instance = RequestContext(request))


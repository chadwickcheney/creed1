from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .forms import PilotForm
from .models import Site, Pilot, Comment

import datetime

class IndexView(generic.ListView):
    template_name = 'assure/index.html'
    context_object_name = 'latest_site_list'
    fields = ['url']
    form_class = PilotForm
    model = Site

    def __init__(self):
        self.creed = None

    def get_queryset(self):
        """Return the last five published sites."""
        return Site.objects.order_by('-pub_date')[:5]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_site_list'] = Site.objects.all()
        context.update({'form':self.form_class})
        return context

    def post(self, request):
        if request.method == 'POST':
            site=''
            url=''
            form = PilotForm(request.POST)
            if form.is_valid():
                url,url_test = self.validate_url(request.POST.get('url'))
                print(url)
                print(url_test)
            try: #fails = site is new and requires a report
                site = Site.objects.get(url__contains=url)
            except Site.DoesNotExist:
                site = Site(url=url,pub_date=datetime.datetime.now())
                site.save()
                return HttpResponseRedirect(reverse('assure:detail', args=(site.id,)))

        return HttpResponseRedirect(reverse('assure:detail', args=(site.id,)))

        #return self.render_to_response(self.get_context_data(context_object_name=self.context_object_name, form=form))

    def validate_url(self, url):
        import re
        regex = re.compile(
            r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE
        )
        return url,re.match(regex, url) is not None

class DetailView(generic.DetailView):
    model = Site
    template_name = 'assure/detail.html'

class ResultsView(generic.DetailView):
    model = Site
    template_name = 'assure/results.html'

def comment(request, site_id):
    site = get_object_or_404(Site, pk=site_id)
    try:
        selected_choice = site.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the site voting form.
        return render(request, 'assure/detail.html', {
            'site': site,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('assure:results', args=(site.id,)))

from django.shortcuts import render
# Create your views here.



from django.shortcuts import render
from webapp.models import sentences
def hello_world(request):
    ss = sentences(journal_id=1,wikilable = 0,crowdlable=1)
    ss.save()
    return render(request, 'claimcheck.html', {})

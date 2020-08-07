from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import sentences
from django.db import connection
import random
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect

def hello_world(request):

    while True:
        t1 = sentences.objects.filter(crowdlabel__isnull=True)
        if (t1.count() == 0):
            continue
        sentence1 = t1[random.randint(0 , t1.count())]
        #print(sentence1.journal_id,sentence1.sentence,sentence1.wikilable)
        dic1 = {"id":sentence1.id,"sentence":sentence1.sentence}
        t2 = sentences.objects.filter(Q(journal_id=sentence1.journal_id) & ~Q(wikilabel=sentence1.wikilabel) & Q(crowdlabel__isnull=True))
        if (t2.count() > 0):
            sentence2 = t2[random.randint(0, t2.count()-1)]
            #print(sentence2.journal_id, sentence2.sentence, sentence2.wikilable)
            dic2= {"id": sentence2.id, "sentence": sentence2.sentence}
            break
        else:
            pass
    logs = [dic1,dic2]
    random.shuffle(logs)
    return render(request, 'claimcheck.html', {"logs":logs})


def savedata(request):
    if request.method == 'POST':
        chosen_claim = request.POST.get('select', '')
        chosen_normal = request.POST.get('2', '') if request.POST.get('1', '') == chosen_claim else request.POST.get('1', '')
        #print("{} choosen as claim and {} as normal sentence".format(chosen_claim, chosen_normal))
        claimlabel = sentences.objects.get(id=chosen_claim)
        claimlabel.crowdlabel = 1
        claimlabel.save()
        nonclaimlabel = sentences.objects.get(id=chosen_normal)
        nonclaimlabel.crowdlabel = 0
        nonclaimlabel.save()
    return HttpResponseRedirect("/")

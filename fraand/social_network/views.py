from django.http import HttpResponse
from django.template import loader

from .models import Item


def index(request):
    items = Item.objects.order_by('-created_at').all()
    context = {'items_results': items}
    template = loader.get_template('index.html')
    return HttpResponse(template.render(context, request))
    # return render(request, 'index.html', context=context)

import logging

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from .models import Item
from .forms import ItemImageFormSet, ItemForm


def index(request):
    items = Item.objects.order_by('-created_at').all()
    context = {'items_results': items}
    template = loader.get_template('index.html')
    return HttpResponse(template.render(context, request))


@login_required
def search(request):
    name_filter = request.POST.get('name', '').strip()
    if len(name_filter) == 0:
        name_filter = request.GET.get('name', '').strip()

    items = Item.objects.filter(name__icontains=name_filter)
    page_number = request.GET.get('page', 1)
    paginate_result = do_paginate(items, page_number)

    paginated_items = paginate_result[0]
    paginator = paginate_result[1]
    base_url = f'/search/?name={name_filter}&'
    context = {
        'items_results': paginated_items,
        'paginator': paginator,
        'base_url': base_url,
        'search_item_name': name_filter
    }
    return render(request=request,
                  template_name='widgets/search_results.html',
                  context=context)


def do_paginate(data_list, page_number):
    ret_data_list = data_list
    # suppose we display at most 2 records in each page.
    result_per_page = 2
    # build the paginator object.
    paginator = Paginator(data_list, result_per_page)
    try:
        # get data list for the specified page_number.
        ret_data_list = paginator.page(page_number)
    except EmptyPage:
        # get the lat page data if the page_number is bigger than last page number.
        ret_data_list = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        # if the page_number is not an integer then return the first page data.
        ret_data_list = paginator.page(1)
    return [ret_data_list, paginator]


class AddItemView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Item
    template_name = 'widgets/item_add.html'
    success_url = '/'
    success_message = 'Item [%(name)s] added successfully!'
    form_class = ItemForm

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, )

    def get(self, request, *args, **kwargs):
        self.object = None

        form_class = self.get_form_class()
        form = self.get_form(form_class)

        return self.render_to_response(
            context=self.get_context_data(form=form)
        )

    def post(self, request, *args, **kwargs):
        self.object = None

        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(AddItemView, self).get_context_data(**kwargs)

        if self.request.POST:
            context['images_form'] = ItemImageFormSet(self.request.POST, self.request.FILES)
        else:
            context['images_form'] = ItemImageFormSet()

        return context

    def form_valid(self, form):
        # Auto-assign `owner_uid` as the current user...
        # TODO: It should be a raw UUID in the future instead of User object...
        form.instance.owner_uid = self.request.user

        # Add images fields [reading]...
        context = self.get_context_data()
        images_form = context['images_form']
        context['success_notification'] = True

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if images_form.is_valid():
                images_form.instance = self.object
                images_form.save()

        return super(AddItemView, self).form_valid(form)

        # TODO: For some reason, it tells...
        #     "Upload a valid image. The file you uploaded was either not an image or a corrupted image."
        # return self.render_to_response(self.get_context_data(form=form, images_form=images_form, success_notification=True))


class GetItemView(LoginRequiredMixin, DetailView):
    model = Item
    template_name = 'widgets/item_detail.html'


class EditItemView(LoginRequiredMixin, UpdateView):
    model = Item
    fields = '__all__'
    template_name = 'widgets/item_edit.html'
    success_url = '/'


class DeleteItemView(LoginRequiredMixin, DeleteView):
    model = Item
    template_name = 'widgets/item_confirm_delete.html'
    success_url = '/'

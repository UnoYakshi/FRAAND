from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView

from .forms import ItemForm, ItemImageFormSet
from .models import Item, Deal


def index(request):
    items_to_display = Item.objects.order_by('-created_at').all()

    context = {'items_results': items_to_display}
    template = loader.get_template('index.html')

    return HttpResponse(template.render(context, request))


@login_required
def search(request):
    name_filter = request.POST.get('name', '').strip()
    if len(name_filter) == 0:
        name_filter = request.GET.get('name', '').strip()

    # Filter by name (case insensitive)...
    name_filtered_items = Item.objects.filter(name__icontains=name_filter)
    # ...and user ID != current user...
    non_items = name_filtered_items.exclude(owner_uid=request.user)
    # ...and non-reserved...
    items_to_display = non_items.exclude(rent=True)

    page_number = request.GET.get('page', 1)
    paginate_result = do_paginate(items_to_display, page_number)
    paginated_items = paginate_result[0]
    paginator = paginate_result[1]

    base_url = f'/search/?name={name_filter}&'
    context = {
        'items_results': paginated_items,
        'paginator': paginator,
        'base_url': base_url,
        'search_item_name': name_filter,
    }
    return render(request=request, template_name='widgets/search_results.html', context=context)


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
        return self.success_message % dict(
            cleaned_data,
        )

    def get(self, request, *args, **kwargs):
        self.object = None

        form_class = self.get_form_class()
        form = self.get_form(form_class)

        return self.render_to_response(context=self.get_context_data(form=form))

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


@login_required
def rent(request, item_id: str):
    """A request to borrow an item from one user to another..."""

    borrower = request.user
    item = Item.objects.get(pk=item_id)
    item_owner = item.owner_uid

    assert borrower != item_owner

    new_deal = Deal.objects.create(
        from_user_uid=item_owner.id, to_user_uid=borrower.id,
        item_uid=item.id,
        status=Deal.DealStatus.INIT
    )
    item.rent = True
    item.save()

    contacts = item.get_contacts().items()

    context = {
        'deal': new_deal,
        'contacts': contacts,
        'success_notification': True
    }

    return render(request, template_name='widgets/rent_add.html', context=context)


class GetRentView(LoginRequiredMixin, DetailView):
    model = Deal
    template_name = 'widgets/rent_detail.html'


class EditRentView(LoginRequiredMixin, UpdateView):
    model = Deal
    fields = '__all__'
    template_name = 'widgets/rent_edit.html'
    success_url = '/'


class DeleteRentView(LoginRequiredMixin, DeleteView):
    model = Deal
    template_name = 'widgets/rent_confirm_delete.html'
    success_url = '/'

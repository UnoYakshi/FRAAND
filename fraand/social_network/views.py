from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView

from .forms import ItemForm, ItemImageFormSet
from .models import Item, Deal


def index(request):
    items_to_display = Item.objects.order_by('-created_at').all()
    context = {'items_results': items_to_display, 'deals_selected': True}

    # template = loader.get_template('index.html')
    template = loader.get_template('cirrus/index.html')
    # template = loader.get_template('cirrus/test.html')

    return render_items(request, items_to_render=items_to_display)

    # return HttpResponse(template.render(context, request))


@login_required
def profile_deals(request):
    context = {
        'user_deals_selected': True,
        'to_you_deals': Deal.objects.filter(to_user_uid=request.user.id),
        'from_you_deals': Deal.objects.filter(from_user_uid=request.user.id)
    }
    template = loader.get_template('cirrus/profile/deals.html')

    return HttpResponse(template.render(context, request))


@login_required
def profile_items(request):
    context = {
        'user_items_selected': True,
        'user_items': Item.objects.filter(owner_uid=request.user.id),
    }
    template = loader.get_template('cirrus/profile/items.html')

    return HttpResponse(template.render(context, request))


@login_required
def profile_settings(request):
    template = loader.get_template('cirrus/profile/settings.html')
    context = {'user_settings_selected': True}
    return HttpResponse(template.render(context, request))


@login_required
def profile_security(request):
    template = loader.get_template('cirrus/profile/security.html')
    context = {'user_security_selected': True}
    return HttpResponse(template.render(context, request))


@login_required
def render_items(request, items_to_render, query: str = ''):
    page_number = request.GET.get('page', 1)
    paginate_result = do_paginate(items_to_render, page_number, result_per_page=3)
    paginated_items = paginate_result[0]
    paginator = paginate_result[1]

    base_url = f'/search/?name={query}&'
    context = {
        'items_results': paginated_items,
        'paginator': paginator,
        'base_url': base_url,
        'search_item_name': query,
    }
    return render(request=request, template_name='cirrus/search_results.html', context=context)


@login_required
def search(request):
    name_filter = request.POST.get('name', '').strip()
    if not name_filter:
        name_filter = request.GET.get('name', '').strip()

    if name_filter:
        # Filter by...
        items_to_display = Item.objects.filter(
            Q(name__icontains=name_filter) |  # ...name (case insensitive)...
            Q(description__icontains=name_filter)  # ...description (case insensitive)...
        ).exclude(
            owner_uid=request.user  # ...and user ID != current user...
        ).exclude(
            rent=True  # ...and non-reserved...
        )
    else:
        items_to_display = []

    return render_items(request, items_to_render=items_to_display, query=name_filter)


def do_paginate(data_list, page_number, result_per_page: int = 3):
    ret_data_list = data_list
    # suppose we display at most 2 records in each page.
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
    template_name = 'cirrus/items/add.html'
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
    template_name = 'cirrus/items/detail.html'


class EditItemView(LoginRequiredMixin, UpdateView):
    model = Item
    fields = ['name', 'description', 'public', 'city', 'tags']
    template_name = 'cirrus/items/edit.html'
    success_url = '/'


class DeleteItemView(LoginRequiredMixin, DeleteView):
    model = Item
    template_name = 'cirrus/items/confirm_delete.html'
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


@login_required
def confirm_rent(request, pk: str):
    deal = Deal.objects.get(pk=pk)
    deal.status = Deal.DealStatus.PENDING

    # assert deal.to_user_uid != request.user

    context = {
        'deal': deal,
        'success_notification': True
    }

    return render(request, template_name='widgets/rent_confirm.html', context=context)


@login_required
def give_away(request, from_uid: str, to_uid: str, item_uid: str):
    assert from_uid != to_uid
    assert request.user == from_uid

    item = Item.objects.get(pk=item_uid)
    item.owner_uid = to_uid
    item.save()

    deal = Deal.objects.get()

    context = {
        'item': item,
        'from_uid': from_uid,
        'to_uid': to_uid,
        'deal': deal
    }

    # Remove the deal?..
    ...

    return render(request, template_name='widgets/wip.html')


@login_required
def change_due_item(request, pk: str):
    return render(request, template_name='widgets/wip.html')


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

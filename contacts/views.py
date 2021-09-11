from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Contact
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.contrib import messages


def index(request):
    contacts = Contact.objects\
            .order_by('name')\
            .filter(show=True)
    paginator = Paginator(contacts, 5)
    page = request.GET.get('page')
    contacts = paginator.get_page(page)
    return render(
        request,
        'contacts/index.html',
        {
            "contacts": contacts
        }
    )


def detail(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id)
    if not contact.show:
        raise Http404()
    return render(
        request,
        'contacts/detail.html',
        {
            'contact': contact
        }
    )


def search(request):
    term = request.GET.get('term')

    if term is None or not term:
        messages.add_message(
            request,
            messages.ERROR,
            "Search field can't be empty."
        )
        return redirect('index')

    concat = Concat('name', Value(' '), 'last_name')
    contacts = Contact.objects.annotate(
        full_name=concat
    ).filter(
        Q(full_name__icontains=term) | Q(phone__icontains=term)
    )
    paginator = Paginator(contacts, 5)
    page = request.GET.get('page')
    contacts = paginator.get_page(page)
    return render(
        request,
        'contacts/search.html',
        {
            "contacts": contacts
        }
    )

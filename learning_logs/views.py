from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404

from django.http import HttpResponseRedirect
# from django.core.urlresolvers import reverse  ---->don't work this modul
from django.urls import reverse

from .models import Topic, Entry
from .forms import TopicForm, EntryForm


# Create your views here.
def index(request):
    """Домашняя страница приложения Learning Log"""
    return render(request, 'learning_logs/index.html')


def check_topic_owner(owner, request):
    if owner != request.user:                       # Ex 19 - 3
        raise Http404


@login_required
def topics(request):
    """Show all topics."""
    # topics = Topic.objects.order_by('date_added')
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)


@login_required
def topic(request, topic_id):
    """Show a single topic, and all its entries."""
    topic = get_object_or_404(Topic, id=topic_id)
    # topic = Topic.objects.get(id=topic_id)
    # Check that the topic belongs to the current user.

    # if topic.owner != request.user:
    #     raise Http404

    check_topic_owner(topic.owner, request)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)


@login_required
def new_topic(request):
    """Defines a new topic."""
    if request.method != 'POST':
        # No data was sent; an empty form is created.
        form = TopicForm()
    else:
        # data was sent POST; form is created.
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            # form.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))

    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    """Adds a new post on a specific topic."""
    # topic = Topic.objects.get(id=topic_id)
    topic = get_object_or_404(Topic, id=topic_id)
    check_topic_owner(topic.owner, request)               #Ex 19-4
    if request.method != 'POST':
        # No data was sent; an empty form is created.
        form = EntryForm()
    else:
        # data was sent POST; form is created.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_logs:topic',
                                                args=[topic_id]))
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    """Edits an existing entry."""
    # entry = Entry.objects.get(id=entry_id)
    entry = get_object_or_404(Entry, id=entry_id)
    topic = entry.topic

    # if topic.owner != request.user:
    #     raise Http404

    check_topic_owner(topic.owner, request)
    if request.method != 'POST':
        # Original request; the form is filled with the data of the current record.
        form = EntryForm(instance=entry)
    else:
        # Sending POST data; process the data.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(
                'learning_logs:topic', args=[topic.id]))

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)







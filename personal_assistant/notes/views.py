"""
Views for managing notes, tags, and note details.
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import TagForm, NoteForm
from .models import Tag, Note


# Create your views here.
@login_required
def notes_view(request):
    """Display a list of notes, with optional search and tag filtering."""
    query = request.GET.get("q", "")
    search_tag = request.GET.get("tag")
    notes = Note.objects.filter(user=request.user)
    if query:
        notes = notes.filter(name__icontains=query)
    if search_tag:
        notes = notes.filter(tags__name__icontains=search_tag).order_by('-created')

    return render(request, 'notes/notes.html', {"notes":notes})


@login_required
def tag(request):
    """Create a new tag for the user."""
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            # form.save()
            tag = form.save(commit=False)
            tag.user = request.user
            tag.save()
            return redirect(to='notes:notes')
        else:
            return render(request, 'notes/tag.html', {'form': form})

    return render(request, 'notes/tag.html', {'form': TagForm()})

@login_required
def note(request):
    """Create a new note for the user, with tags."""
    tags = Tag.objects.filter(user=request.user).all()

    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            new_note = form.save(commit=False)
            new_note.user = request.user
            new_note.save()
            choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'), user=request.user)

            for tag in choice_tags.iterator():
                new_note.tags.add(tag)

            return redirect(to='notes:notes')
        else:
            return render(request, 'notes/notes_form.html', {"tags": tags, 'form': form})

    return render(request, 'notes/notes_form.html', {"tags": tags, 'form': NoteForm()})

@login_required
def detail(request, note_id):
    """Display the details of a specific note."""
    note = get_object_or_404(Note, pk=note_id, user=request.user)

    return render(request, 'notes/detail.html', {"note": note})


@login_required
def delete_note(request, note_id):
    """Delete a specific note for the user."""
    Note.objects.get(pk=note_id, user=request.user).delete()
    return redirect(to='notes:notes')

@login_required
def edit_note(request, note_id):
    """Edit an existing note for the user."""
    note = get_object_or_404(Note, id=note_id, user=request.user)

    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('notes:notes')
    else:
        form = NoteForm(instance=note)
    return render(request, 'notes/edit_note.html', {'form': form})
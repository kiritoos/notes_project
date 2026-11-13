from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from .forms import NoteForm
from .models import Note
from .services import get_categories_with_counts  # Импорт кэша

def index(request):
    notes = Note.objects.select_related("category", "owner").prefetch_related("tags")
    if request.GET.get("category"):
        notes = notes.filter(category_id=request.GET["category"])
    if request.GET.get("active"):
        notes = notes.filter(is_done=False)
    if request.GET.get("q"):
        notes = notes.filter(title__icontains=request.GET["q"])

    paginator = Paginator(notes, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    # Используем кэш вместо прямого запроса
    categories = get_categories_with_counts()
    
    return render(request, "notes/note_list.html", {
        "page": page_obj, "categories": categories,
    })

def note_create(request):
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("notes:index")
    else:
        form = NoteForm()
    return render(request, "notes/note_form.html", {"form": form, "title": "Новая заметка"})

def note_update(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == "POST":
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect("notes:index")
    else:
        form = NoteForm(instance=note)
    return render(request, "notes/note_form.html", {"form": form, "title": "Редактирование"})

def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == "POST":
        note.delete()
        return redirect("notes:index")
    return render(request, "notes/note_confirm_delete.html", {"note": note})
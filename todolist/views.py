from django.shortcuts import render

def todo_list(request):
    pass

def todo_detail(request, todo_id):
    return render(request, 'todo_detail.html')


def todo_create(request):
    return render(request, 'todo_create.html')

def todo_update(request, todo_id):
    pass


def todo_delete(request, todo_id):
    pass


def todo_complete(request, todo_id):
    pass


def todo_uncomplete(request, todo_id):
    pass


def todo_archived(request, todo_id):
    pass


def todo_search(request, todo_id):
    pass

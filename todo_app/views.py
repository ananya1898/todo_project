# todo_app/views.py
from django.urls import reverse, reverse_lazy
from django.views.generic import (ListView, CreateView, UpdateView, DeleteView)
from .models import ToDoList, ToDoItem
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages



# Implementation for viewing lists and items corresponding to that list
class ListListView(ListView):
    model = ToDoList
    template_name = "todo_app/index.html"

    def get_queryset(self):
        return ToDoList.objects.filter(username=self.request.user)


class ItemListView(ListView):
    model = ToDoItem
    template_name = "todo_app/todo_list.html"

    def get_queryset(self):
        return ToDoItem.objects.filter(todo_list_id=self.kwargs["list_id"])

    def get_context_data(self):
        context = super().get_context_data()
        context["todo_list"] = ToDoList.objects.get(id=self.kwargs["list_id"])
        return context


# Creating new list


class ListCreate(CreateView):
    model = ToDoList
    fields = ["title"]

    def get_context_data(self):
        context = super(ListCreate, self).get_context_data()
        context["title"] = "Add a new list"
        context["username"] = self.request.user
        return context
    def form_valid(self, form):
        form.instance.username = self.request.user
        return super().form_valid(form)

# Creating a new item in the list

class ItemCreate(CreateView):
    model = ToDoItem
    fields = ["todo_list", "title", "description", "due_date"]

    def get_initial(self):
        initial_data = super(ItemCreate, self).get_initial()
        todo_list = ToDoList.objects.get(id=self.kwargs["list_id"])
        initial_data["todo_list"] = todo_list
        return initial_data

    def get_context_data(self):
        context = super(ItemCreate, self).get_context_data()
        todo_list = ToDoList.objects.get(id=self.kwargs["list_id"])
        context["todo_list"] = todo_list
        context["title"] = "Create a new item"
        return context

    def get_success_url(self):
        return reverse("list", args=[self.object.todo_list_id])


class ItemUpdate(UpdateView):
    model = ToDoItem
    fields = [
        "todo_list",
        "title",
        "description",
        "due_date",
        "is_completed"
    ]

    def get_context_data(self):
        context = super(ItemUpdate, self).get_context_data()
        context["todo_list"] = self.object.todo_list
        context["title"] = "Edit item"
        return context

    def get_success_url(self):
        return reverse("list", args=[self.object.todo_list_id])


# Delete a list and item

# todo_list/todo_app/views.py
class ListDelete(DeleteView):
    model = ToDoList
    # You have to use reverse_lazy() instead of reverse(),
    # as the urls are not loaded when the file is imported.
    success_url = reverse_lazy("index")


class ItemDelete(DeleteView):
    model = ToDoItem

    def get_success_url(self):
        return reverse_lazy("list", args=[self.kwargs["list_id"]])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["todo_list"] = self.object.todo_list
        return context


# OverDueTask Email

class SendEmail:

    @classmethod
    def send_email(self, task_title, task_due_date):
        subject = 'Reminder To Complete Your Task'
        message = 'Hello,\n\nYou have not completed your task ' + task_title + ' yet.\nThe due date for the same was ' + str(
            task_due_date.date()) + '.\n' + 'Please complete it as soon as possible.\nIf you wish to change the due date go to xyz.\n\n' + 'Thanks\n'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = ['ananyadps18@gmail.com']
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

    @classmethod
    def identify_overdue_tasks_and_send_email(self):
        all_tasks = ToDoItem.objects.all()
        for task in all_tasks:
            if not task.is_completed and task.due_date.date() == timezone.now().date():
                self.send_email(task.title, task.due_date)


class User:
    def register_request(request):
        if request.method == "POST":
            form = NewUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                messages.success(request, "Registration successful.")
                return redirect("main:homepage")
            messages.error(request, "Unsuccessful registration. Invalid information.")
        form = NewUserForm()
        return render(request=request, template_name="todo_app/register.html", context={"register_form": form})

    def login_request(request):

        if request.method == "POST":
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.info(request, f"You are now logged in as {username}.")
                    return redirect("index")
                else:
                    messages.error(request, "Invalid username or password.")
            else:
                messages.error(request, "Invalid username or password.")
        form = AuthenticationForm()

        return render(request=request, template_name="todo_app/login.html", context={"login_form": form})

    def logout_request(request):
        logout(request)
        messages.info(request, "You have successfully logged out.")
        return redirect("login")
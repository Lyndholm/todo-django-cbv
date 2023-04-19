from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db import transaction
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, FormView, UpdateView
from django.views.generic.list import ListView

from .forms import TaskPositionForm
from .models import Task


class RegisterView(FormView):
    form_class = UserCreationForm
    template_name = 'base/register.html'
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterView, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterView, self).get(*args, **kwargs)


class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)

        query = self.request.GET.get('query') or ''
        if query:
            context['tasks'] = context['tasks'].filter(title__contains=query)

        context['count'] = context['tasks'].filter(complete=False).count()
        context['query_value'] = query

        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'

    def dispatch(self, *args, **kwargs):
        task = self.get_object()
        if task.user != self.request.user:
            raise Http404
        return super().dispatch(*args, **kwargs)


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = (
        'title',
        'description',
        'complete',
    )
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = (
        'title',
        'description',
        'complete',
    )
    success_url = reverse_lazy('tasks')

    def dispatch(self, *args, **kwargs):
        task = self.get_object()
        if task.user != self.request.user:
            raise Http404
        return super().dispatch(*args, **kwargs)


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')

    def dispatch(self, *args, **kwargs):
        task = self.get_object()
        if task.user != self.request.user:
            raise Http404
        return super().dispatch(*args, **kwargs)


class TaskReorder(View):
    def post(self, request):
        form = TaskPositionForm(request.POST)

        if form.is_valid():
            task_positions = form.cleaned_data.get('position').split(',')

            with transaction.atomic():
                self.request.user.set_task_order(task_positions)

        return redirect(reverse_lazy('tasks'))

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, AccountUpdateForm,  AddExercise, UserProgrammeForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .tables import ProgrammeTable
from .models import Programme, Post
from django_tables2.config import RequestConfig
from django_tables2.export.export import TableExport
import pickle
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'users/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'users/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    #making sure author of post is the one updating it
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'users/about.html', {'title': 'About'})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        # bw_form = UserBodyweightForm(request.POST)
        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
        # bw_form = UserBodyweightForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        a_form = AccountUpdateForm(request.POST, request.FILES, instance=request.user.account)

        if u_form.is_valid() and a_form.is_valid():
            u_form.save()
            a_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        a_form = AccountUpdateForm(instance=request.user.account)

    context = {
        'u_form': u_form,
        'a_form': a_form
    }

    return render(request, 'users/profile.html', context)



@login_required
def log_programme(request):
    if request.method == 'POST':
        c = {}
        programme_form = UserProgrammeForm(request.POST)

        if programme_form.is_valid():

            pr = programme_form.save(commit=False)
            pr.lifter_id = request.user.id
            pr.save()

            messages.success(request, f'Your workout has been updated with {pr.exercise} : '
                                      f'{pr.sets} x {pr.reps} @ {pr.weight}Kg on {pr.date}!')
        else:
            c['date'] = programme_form.date

            return redirect('log-programme', c)
    else:
        programme_form = UserProgrammeForm()

    context = {
          'pr_form': programme_form,
         

      }
    return render(request, 'users/createprogramme.html', context)



def add_exercise(request):
    template_name = 'users/addexercise.html'
    if request.method == 'POST':

        exercise_form = AddExercise(request.POST)

        if exercise_form.is_valid():

            exercise_form.save()
            name = exercise_form.cleaned_data.get('name')

            messages.success(request, f'{name} has been added!')
            return redirect('log-programme')
    else:

        exercise_form = AddExercise()

    context = {
          'exercise_form': exercise_form

      }

    return render(request, template_name, context)


@login_required
def dashboard(request):

        programme_dashboard = ProgrammeTable(Programme.objects.filter(lifter_id=request.user.id))

        RequestConfig(request).configure(programme_dashboard)

        export_format = request.GET.get('_export', None)
        if TableExport.is_valid_format(export_format):
            exporter = TableExport(export_format, programme_dashboard)
            return exporter.response('programme_dashboard.{}'.format(export_format))

        return render(request, 'users/dashboard.html', {
            'programme_dashboard': programme_dashboard
        })


@login_required()
def generate_prediction(request):

    # get users data from Programme
    programme_data_unfiltered = ProgrammeTable(Programme.objects.filter(lifter_id=request.user.id))



    # filter data so only pulling exercise = 'back squat', 'front squat' and ('snatch'+'clean&jerk') which we alias as 'Total'

   # if programme_data_unfiltered.exercise == 'Back Squat' & programme_data_unfiltered.sets == 1:

   # if programme_data_unfiltered.exercise == 'Front Squat' & programme_data_unfiltered.sets == 1:


    # export data to csv

    # load data to model and make prediction

    loaded_model = pickle.load(open('C:/new_model.sav', 'rb'))

    result = loaded_model.predict(new_data)

    # return prediction
    return render(request, '', {'': result})
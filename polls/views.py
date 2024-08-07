from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .models import Question, Choice
from django.urls import reverse, reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate , logout
from .forms import SignUpForm

def home_view(request):
    """
    Renders the home page.

    Args:
        request: The HTTP request object.

    Returns:
        The rendered home page.
    """
    return render(request, 'polls/home.html')


def index(request):
    """
    Renders the home page with the latest questions.

    Args:
        request: The HTTP request object.

    Returns:
        The rendered index page with the latest questions.
    """
    # Fetch the latest questions and pass them to the template
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    """
    Renders the detail page for a specific question.

    Args:
        request: The HTTP request object.
        question_id: The ID of the question.

    Returns:
        The rendered detail page for the specified question.
    """
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    """
    Renders the results page for a specific question.

    Args:
        request: The HTTP request object.
        question_id: The ID of the question.

    Returns:
        The rendered results page for the specified question.
    """
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


@login_required
def vote(request, question_id):
    """
    Handles the voting process for a specific question.

    Args:
        request: The HTTP request object.
        question_id: The ID of the question.

    Returns:
        An HttpResponseRedirect to the results page after a successful vote,
        or re-renders the voting page with an error message if no choice was selected.
    """
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form with an error message
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice."
        })
    else:
        # Increment the vote count and save the selected choice
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing with POST data.
        # This prevents data from being posted twice if a user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))


def signup(request):
    """
    Handles user signup.

    Args:
        request: The HTTP request object.

    Returns:
        Renders the signup page with a form, or redirects to the home page after successful signup.
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data.get('first_name')
            user.email = form.cleaned_data.get('email')
            user.save()
            # Retrieve the username and password from the cleaned form data
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            # Authenticate and log in the user
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            # Redirect to the home page after successful login
            return redirect('home')
        else:
            print(form.errors)  # Print form errors for debugging
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def logout_view(request):
    """
    Log out the user and redirect to the home page.

    This view logs out the currently authenticated user by calling Django's 
    built-in `logout` function. After logging out, the user is redirected 
    to the home page.

    Args:
        request (HttpRequest): The request object used to generate this response.

    Returns:
        HttpResponseRedirect: A redirect to the home page.
    """
    logout(request)
    return redirect('home')


def register(request):
    """
    Handles user registration.

    Renders registration form on GET request. 
    Processes form submission on POST request, saves user if valid,
    and logs them in.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Rendered HTML template for registration or redirects to home.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')  # Replace 'home' with the name of your home URL pattern
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})  


class MyLoginView(LoginView):
    """
    Custom login view for handling user authentication.

    Attributes:
        template_name (str): The path to the login template.
        redirect_authenticated_user (bool): Whether to redirect authenticated users.
        success_url (str): The URL to redirect to after a successful login.
    """
    template_name = 'registration/login.html'  # Specify the template
    redirect_authenticated_user = True  # Redirect users if already authenticated
    success_url = reverse_lazy('home')  # Redirect after successful login    

 
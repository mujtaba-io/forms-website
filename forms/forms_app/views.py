from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from .models import *


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.get(email=email)
        if user is not None:
            if user.password == password:
                request.session['user_pk'] = user.pk
                return redirect('dashboard')
            else:
                return redirect('login')

    return render(request, 'login.html')


def signup_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not User.objects.filter(email=email).exists():
            # Create a new user
            user = User(email=email, password=password)
            user.save()

            request.session['user_pk'] = user.pk
            return redirect('dashboard')
        else:
            # User already exists
            return redirect('signup')  # Replace 'signup' with the URL name for your signup page

    return render(request, 'signup.html')


def dashboard_view(request):
    user = User.objects.get(pk=request.session['user_pk'])
    forms = Form.objects.filter(user=user)
    if request.method == 'POST':
        pass  # Handle the form submission here


    context = {
        'forms': forms
    }
    return render(request, 'dashboard.html', context)



def form_details(request, form_name):
    user_pk = request.session.get('user_pk')
    form = Form.objects.filter(name=form_name, user_id=user_pk).first()

    if form:
        if request.method == 'POST':
            question_text = request.POST.get('question_text')
            question_type = request.POST.get('question_type')
            checkbox_responses = request.POST.getlist('checkbox_responses')
            radio_responses = request.POST.getlist('radio_responses')

            # Store the retrieved data in variables
            # You can perform further processing or save them to models later

            # Example printing the data
            print("Question Text:", question_text)
            print("Question Type:", question_type)
            print("Checkbox Responses:", checkbox_responses)
            print("Radio Responses:", radio_responses)

            new_question = Question(text=question_text, type=question_type, form=form)
            new_question.save()

            if question_type == 'checkbox':
                for response in checkbox_responses:
                    new_choice = Choice(text=response, question=new_question)
                    new_choice.save()
            elif question_type == 'radio':
                for response in radio_responses:
                    new_choice = Choice(text=response, question=new_question)
                    new_choice.save()

        questions = Question.objects.filter(form=form)
        context = {'form': form, 'questions': questions}
        return render(request, 'form_details.html', context)
    else:
        # Handle case when form is not found
        return redirect('dashboard')


def form_fill(request, form_name):
    form = Form.objects.filter(name=form_name).first()

    if form:
        if request.method == 'POST':
            questions = Question.objects.filter(form=form)
            for question in questions:
                response_key = f'question_{question.pk}_responses'
                response_value = request.POST.get(response_key)
                if response_value is not None:
                    # Save the response to Answer model
                    answer = Answer(text=response_value, question=question)
                    answer.save()

            return redirect('dashboard')  # Redirect to the desired page after submitting the form

        questions = Question.objects.filter(form=form)
        context = {'form_name': form_name, 'questions': questions}
        return render(request, 'form_fill.html', context)
    else:
        # Handle case when form is not found
        return redirect('dashboard')

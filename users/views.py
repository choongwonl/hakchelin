from django.shortcuts import render
from .forms import RegisterForm, AccountForm
from .models import CustomUser
from django.views.generic import TemplateView, UpdateView

# Create your views here.

def register(request):

    if request.method == 'POST':
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'registration/register_done.html', {'new_user' : new_user})
    else:
        user_form = RegisterForm()

    return render(request, 'registration/register.html',{'form':user_form})

def account(request):
    if request.method == "GET":
        user_form= AccountForm(instance=request.user)
        
    elif request.method == "POST":
        user_form = AccountForm(request.POST)
        account_form = AccountForm(request.POST, instance=request.user)
        #if user_form.is_valid():
        user = request.user
        # new_user = user_form.save(commit=True)
        user.update(email=user_form['email']) 
        user.update(password= user_form['password']) 
        return render(request, 'registration/register_done.html', {'new_user' : user})
    else:
        user_form = AccountForm()

    return render(request, 'registration/register.html',{'form':user_form})

class UpdateProfile(UpdateView):
    model = CustomUser
    fields = ['email', 'name']

    template_name = 'registration/account.html'

    def get_object(self):
        return self.request.user
        
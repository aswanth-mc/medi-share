from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model

User = get_user_model()


def welcome_view(request):
    return render(request, 'welcome.html')


# def user_login(request):

#     if request.user.is_authenticated:

#         if request.user.role == 'admin':
#             return redirect('admin_dashboard')

#         elif request.user.role == 'unit':
#             return redirect('unit_dashboard')

#         return redirect('user_dashboard')

#     if request.method == "POST":

#         email = request.POST.get('email')
#         password = request.POST.get('password')

#         try:
#             user_obj = User.objects.get(email=email)

#         except User.DoesNotExist:
#             user_obj = None

#         if user_obj:

#             user = authenticate(
#                 request,
#                 username=user_obj.username,
#                 password=password
#             )

#             if user is not None:

#                 login(request, user)

#                 if user.role == 'admin':
#                     return redirect('admin_dashboard')

#                 elif user.role == 'unit':
#                     return redirect('unit_dashboard')

#                 return redirect('user_dashboard')

#         return render(request, 'login.html', {
#             'error': 'Invalid email or password'
#         })

#     return render(request, 'login.html')

def user_login(request):
    return render(request, 'auth/login.html')

def register_choice(request):
    return render(request, 'auth/register_choice.html')
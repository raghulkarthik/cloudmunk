from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm  # import your custom form
from django.contrib import messages
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.contrib.auth.models import User

from storage.models import File
from .forms import FileUploadForm
from .models import File

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)  # use custom form here
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')
    else:
        form = CustomUserCreationForm()  # and here
    return render(request, 'users/register.html', {'form': form})

def home(request):
    if request.user.is_authenticated:
        return redirect('users:dashboard')  #  Redirect logged-in users to dashboard

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! You can now log in.")
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'home.html', {'form': form})

@login_required
def dashboard(request):
    return render(request, 'users/dashboard.html')

# told by chat
# @login_required
# def upload_file(request):
#     if request.method == 'POST':
#         form = FileUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             file = form.save(commit=False)
#             file.user = request.user  # Save the file owner
#             file.save()

#             # ✅ Check total storage used after upload
#             total = get_total_storage(request.user)
#             if total >= 90 * 1024 * 1024:  # 90 MB threshold
#                 send_mail(
#                     subject='⚠️ Storage Almost Full',
#                     message='You have used 90% of your available storage. Please free up space or upgrade your plan.',
#                     from_email='raghulkarthik21@gmail.com',
#                     recipient_list=[request.user.email],
#                     fail_silently=False,
#                 )

#             return redirect('view_files')
#     else:
#         form = FileUploadForm()
#     return render(request, 'storage/templates/storage/upload.html', {'form': form})


# @login_required
# def upload_file(request):
#     if request.method == 'POST':
#         form = FileUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             file = form.save(commit=False)
#             file.user = request.user  # Save the file owner
#             file.save()
#             return redirect('view_files')
#     else:
#         form = FileUploadForm()
#     return render(request, 'storage/templates/storage/upload.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # ✅ Send login email
            send_mail(
                'Login Notification - Cloud Storage',
                f'Hello {user.username},\n\nYou have successfully logged into your cloud storage account.',
                'yourapp@example.com',  # Replace with your sender email (must be configured in settings)
                [user.email],           # Email goes to the logged-in user's email
                fail_silently=True,
            )

            return redirect('users:dashboard')  # or wherever you go after login
        else:
            return render(request, 'registration/login.html', {'error': 'Invalid credentials'})

    return render(request, 'registration/login.html')

@login_required
def test_email(request):
    send_mail(
        subject='Login Alert',
        message='You have successfully logged into your Cloud Storage account.',
        from_email='raghulkarthik21@gmail.com',
        recipient_list=[request.user.email],  # ✅ Use request.user.email here
        fail_silently=False,
    )
    return HttpResponse("Email sent!")

def get_total_storage(user):
    files = File.objects.filter(user=user)
    return sum(f.file.size for f in files)


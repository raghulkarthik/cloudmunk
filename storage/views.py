from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.core.exceptions import ValidationError
from django.contrib import messages
from .forms import FileUploadForm
from .models import File
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import F
from django.core.mail import send_mail
from django.http import HttpResponse

# Helper function to calculate total storage used by user (in bytes)
def get_user_storage_used(user):
    total_size = user.file_set.aggregate(total=Sum('file__size'))['total']
    return total_size or 0  # Return 0 if None

@login_required
def storage_upload_file(request):
    max_storage = 100 * 1024 * 1024  # 100 MB
    user_files = File.objects.filter(user=request.user)
    used_storage = sum(f.file.size for f in user_files)

    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            if used_storage + uploaded_file.size > max_storage:
                messages.error(request, "Upload failed: You have reached your 100MB storage limit.")
            else:
                try:
                    file = form.save(commit=False)
                    file.user = request.user
                    file.full_clean()
                    file.save()
                    messages.success(request, "File uploaded successfully.")

                    # ✅ Send warning email at 90% usage
                    if used_storage + uploaded_file.size >= 90 * 1024 * 1024:
                        send_mail(
                            subject='⚠️ Storage Almost Full',
                            message='You have used 90% of your available storage. Please free up space or upgrade your plan.',
                            from_email='raghulkarthik21@gmail.com',
                            recipient_list=[request.user.email],
                            fail_silently=True,
                        )

                    return redirect('storage:file_list')
                except ValidationError as e:
                    messages.error(request, e.message_dict.get('file', ['Invalid file'])[0])
        else:
            messages.error(request, "Form is invalid. Please check the uploaded file.")
    else:
        form = FileUploadForm()

    return render(request, 'storage/upload.html', {
        'form': form,
        'used_storage': used_storage / (1024 * 1024),  # in MB
        'max_storage': 100,
    })


@login_required
def storage_file_list(request):
    max_storage = 100 * 1024 * 1024  # 100 MB in bytes

    sort_key = request.GET.get('sort', 'uploaded_at')
    files = File.objects.filter(user=request.user)

    if sort_key == 'file':  # Sort by filename (basename)
        files = sorted(files, key=lambda f: f.file.name.lower())
    elif sort_key == '-file':  # Descending filename
        files = sorted(files, key=lambda f: f.file.name.lower(), reverse=True)
    else:
        # Default ORM sorting by uploaded_at or other fields supported by DB
        if sort_key.lstrip('-') in ['uploaded_at']:
            files = files.order_by(sort_key)

    used_storage = sum(f.file.size for f in files)  # sum file sizes in bytes

    context = {
        'files': files,
        'used_storage': used_storage / (1024 * 1024),  # MB
        'max_storage': max_storage / (1024 * 1024),    # MB
    }

    return render(request, 'storage/file_list.html', context)

@login_required
def delete_file(request, file_id):
    file = get_object_or_404(File, id=file_id, user=request.user)
    if request.method == "POST":
        file.file.delete()  # delete the actual file from storage
        file.delete()       # delete from DB
        messages.success(request, "File deleted successfully.")
    return redirect('storage:file_list')

def test_email(request):
    send_mail(
        subject='Test Email from Django',
        message='If you see this, your Django email setup works!',
        from_email='raghulkarthik21@gmail.com',
        recipient_list=['raghulkarthik21@gmail.com'],
        fail_silently=False,
    )
    return HttpResponse("✅ Test email sent successfully!")
# views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from .models import LitterInstance

@login_required
def user_account(request):
    return render(request, 'user_account.html')

@login_required
def admin_account(request):
    if not request.user.is_admin:
        return HttpResponse("Unauthorized", status=401)
    return render(request, 'admin_account.html')

def approve_litter_instance(request):
    if request.method == 'POST':
        # Assuming you have some way to identify the litter instance to be approved,
        # for example, passing its ID through POST data.
        litter_instance_id = request.POST.get('litter_instance_id')
        litter_instance = LitterInstance.objects.get(id=litter_instance_id)
        litter_instance.approved = True
        litter_instance.save()
        return redirect('admin_account')
    return redirect('admin_account')  # Redirect to admin account page if request method is not POST
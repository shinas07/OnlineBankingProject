from django.shortcuts import redirect, render
from django.http import JsonResponse
from .models import Applicant
from django.contrib.auth.decorators import login_required
from .models import District,Branch
from django.views.decorators.cache import never_cache



    
@never_cache
def home(request):
    return render(request, 'home.html')

    
@never_cache
@login_required(login_url='accounts:login')
def new_page(request):
    return render(request, 'new_page.html')


    
@never_cache
@login_required(login_url='accounts:login')
def show_form(request):
    districts = District.objects.all()
    return render(request, 'form_page.html',{'districts':districts})




@never_cache
def get_branches(request):
    selected_district_id = request.GET.get('district_id')
    branches = Branch.objects.filter(district_id=selected_district_id)
    
    # Serialize Branch queryset into JSON-friendly format
    serialized_branches = [{'id': branch.id, 'name': branch.name} for branch in branches]
    return JsonResponse({'branches': serialized_branches})


@login_required(login_url='accounts:login')
def form_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        dob = request.POST.get('dob')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')
        district = request.POST.get('district')
        branch = request.POST.get('branch')
        account_type = request.POST.get('accountType')
        materials_provided = request.POST.getlist('materials')

        age = int(age)
        if age < 18:
            return JsonResponse({'error': 'You must be at least 18 years old to register.'}, status=400)

        application = Applicant.objects.create(
            name=name,
            dob=dob,
            age=age,
            gender=gender,
            phone=phone,
            email=email,
            address=address,
            district=district,
            branch=branch,
            account_type=account_type,
            materials_provided = materials_provided ,
        )
        application.save()
        return JsonResponse({'message':'Form data received successfully'})
    else:
        return JsonResponse({'error': 'Unsupported request method'}, status=405)

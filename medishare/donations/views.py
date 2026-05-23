from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from donation.models import Donation
from donation.utils import calculate_distance

from unit.models import PalliativeUnit
# Create your views here.


@login_required
def create_donation(request):

    if request.method == 'POST':

        medicine_name = request.POST.get('medicine_name')

        quantity = request.POST.get('quantity')

        expiry_date = request.POST.get('expiry_date')

        description = request.POST.get('description')

        pickup_location = request.POST.get('pickup_location')

        latitude = request.POST.get('latitude')

        longitude = request.POST.get('longitude')

        medicine_image = request.FILES.get('medicine_image')

        verified_units = PalliativeUnit.objects.filter(
            is_verified=True
        )

        nearest_unit = None
        nearest_distance = None

        for unit in verified_units:

            distance = calculate_distance(
                float(latitude),
                float(longitude),
                unit.latitude,
                unit.longitude
            )

            if nearest_distance is None or distance < nearest_distance:

                nearest_distance = distance
                nearest_unit = unit

        Donation.objects.create(
            donor=request.user,
            unit=nearest_unit,
            medicine_name=medicine_name,
            quantity=quantity,
            expiry_date=expiry_date,
            medicine_image=medicine_image,
            description=description,
            pickup_location=pickup_location,
            latitude=latitude,
            longitude=longitude,
        )

        return redirect('user_dashboard')

    return render(
        request,
        'donation/create_donation.html'
    )
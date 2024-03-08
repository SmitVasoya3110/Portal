from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import ContactUs, Feedback

def contact_us(request):
    if request.method == 'POST':
        print(request.POST)
        # Get form data from the request
        username = request.POST.get('username')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Validate if any field is empty
        if not (username and email and message):
            return HttpResponse("All fields are required. Please fill in all the details.")

        # Save data to the ContactUs model
        ContactUs.objects.create(username=username, email=email, message=message)

        return redirect('home')  # Redirect to a success page or another URL

    return render(request, 'contact/contact_us.html')

def feedback(request):
    if request.method == 'POST':
        print(request.POST)
        username = request.POST.get('username')
        email = request.POST.get('email')
        message = request.POST.get('message')
        rating = request.POST.get('rating')

        if not (username and email and message and rating):
            return HttpResponse("All fields are required. Please fill in all the details and provide a rating.")

        Feedback.objects.create(username=username, email=email, message=message, rating=rating)

        return redirect('home')  # Redirect to a success page or another URL

    return render(request, 'contact/feedback.html')
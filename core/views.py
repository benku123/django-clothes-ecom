from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import reverse, render
from django.views import generic
from .forms import ContactForm, NewsForm
from .models import NewsLetter
from .forms import CreateUser
from django.shortcuts import redirect

def home(request):
    if request.method == "POST":
        form = NewsForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            new = NewsLetter.objects.create(email=email)
            new.save()
            messages.info(request, "You have successfully added your Email")
    else:
        form = NewsForm()
    return render(request, 'index.html', {'emailform': form})



class ContactView(generic.FormView):
    form_class = ContactForm
    template_name = 'contact.html'

    def get_success_url(self):
        return reverse("contact")

    def form_valid(self, form):
        messages.info(
            self.request, "Thanks for getting in touch. We have received your message.")
        name = form.cleaned_data.get('name')
        email = form.cleaned_data.get('email')
        message = form.cleaned_data.get('message')

        full_message = f"""
            Received message below from {name}, {email}
            ________________________


            {message}
            """
        send_mail(
            subject="Received contact form submission",
            message=full_message,
            from_email=settings.EMAIL_HOST_USER, #but we dont have password and so settings, so it will be here
            recipient_list=[email]
        )
        return super(ContactView, self).form_valid(form)


def authentication(request):
    form = CreateUser()
    print(request.method)
    if request.method == "POST":
        print(request.method)
        if request.POST.get('submit') == 'register':

            form = CreateUser(request.POST)
            if form.is_valid():
                form.save()
                name = request.POST.get('username')
                messages.success(request, f"account was created for {name}")
                return redirect('home')
            else:
                messages.error(request, "The form is filled wrongly.")
        else:
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:

                messages.info(request, 'Username OR password is incorrect')



    return render(request, "account/login.html", {'form': form})


def logoutUser(request):
    logout(request)
    messages.info(request, "you have logged out successfully")
    return redirect('home')


def staff(request):
    return render(request, "staff.html")
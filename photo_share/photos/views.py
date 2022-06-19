from django.shortcuts import render, redirect
from .models import Category, Photo
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm


# Create your views here.
def login_page_view(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:
            login(request, user)
            return redirect('photos:gallery')

    return render(request, template_name='photos/login_registration.html')


def logout_view(request):
    logout(request)
    return redirect('photos:login')


def register_view(request):
    form = RegisterForm()
    context = {
        'form': form,
        'is_register_page': True
    }

    if request.POST:
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            user = authenticate(
                request,
                username=request.POST['username'],
                password=request.POST['password1'],
            )

            if user:
                login(request, user)
                return redirect('photos:gallery')

    return render(request, template_name='photos/login_registration.html', context=context)


@login_required(login_url='photos:login')
def gallery_view(request):
    user = request.user
    category = request.GET.get('category')

    if category is None:
        photos = Photo.objects.filter(category__user=user)
    else:
        photos = Photo.objects.filter(category__name=category, category__user=user)

    categories = Category.objects.filter(user=user)

    context = {
        'categories': categories,
        'photos': photos
    }
    return render(request, template_name='photos/gallery.html', context=context)


@login_required(login_url='photos:login')
def add_photo_view(request):
    user = request.user
    categories = Category.objects.filter(user=user)
    context = {'categories': categories}

    if request.POST:
        data = request.POST
        if data['category'] != 'none':
            category = Category.objects.get(id=data['category'])
        elif request.POST['new-category']:
            category, create = Category.objects.get_or_create(user=user, name=data['new-category'])
        else:
            category = None

        description = data['description']
        images = request.FILES.getlist('uploaded-images')

        photos = (Photo(category=category, description=description, image=image) for image in images)
        Photo.objects.bulk_create(photos)

        # Photo.objects.create(
        #     category=category,
        #     description=description,
        #     image=image
        # )

        return redirect('photos:gallery')

    return render(request, template_name='photos/add.html', context=context)


@login_required(login_url='photos:login')
def photo_view(request, pk):
    photo = Photo.objects.get(id=pk)

    return render(request, template_name='photos/photo.html', context={'photo': photo})

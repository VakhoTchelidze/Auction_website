from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ItemForm, UserForm, MyUserCreationForm

# Create your views here.
from .models import Category, User, Item, Bid, Collection, Comment
from django.db.models import Q
from django.utils import timezone

# from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.files.storage import FileSystemStorage

# from django.contrib.auth.forms import UserCreationForm

def check_and_transfer_expired_items():
    now = timezone.now()
    expired_items = Item.objects.filter(bid_end_date__lt=now, active=True)
    expired_item_highest_bid = []

    for item in expired_items:
        highest_price_bid = Bid.objects.filter(item__id=int(item.id)).order_by('-bid').first()
        expired_item_highest_bid.append((item, highest_price_bid))

    for item, bid in expired_item_highest_bid:
        Collection.objects.create(
            owner= bid.bidder,
            item= bid.item,
            win_price=bid.bid
        )
        item.active = False
        item.save()


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ""

    check_and_transfer_expired_items()
    categories = Category.objects.all()
    artists = User.objects.filter(is_artist=True)
    items = Item.objects.filter(active=True).filter(Q(category__name__icontains = q) | Q(name__icontains = q) | Q(description__icontains = q))
    item_count = items.count()

    context = {'categories': categories, 'artists': artists, 'items':items, 'item_count': item_count}
    return render(request, 'base\\home.html', context)

def item(request, pk):
    print(pk)
    item = Item.objects.get(id=int(pk))

    categories = Category.objects.all()
    artists = User.objects.filter(is_artist=True)

    if not item.active:
        return HttpResponse('<h1>This item no longer exists!</h1>')

    if Bid.objects.filter(item__id=int(pk)).order_by('-bid').first():
        highest_price_bid = Bid.objects.filter(item__id=int(pk)).order_by('-bid').first()
        highest_price_bid = highest_price_bid.bid
    else:
        highest_price_bid = 0

    try:
        numeber_of_bids = Bid.objects.filter(item__id=int(pk)).count()
    except:
        numeber_of_bids = 0

    comments = Comment.objects.filter(item__id=int(pk))
    comments_count = Comment.objects.filter(item__id=int(pk)).count()


    if request.method == 'POST':
        print(request.POST)
        try:
            if int(request.POST.get('bid')) > item.price and int(request.POST.get('bid')) > highest_price_bid:
                bid = Bid.objects.create(
                    bidder = request.user,
                    item = item,
                    bid = request.POST.get('bid')
                )
                return redirect('item', pk=item.id)
        except:
            pass
        finally:
            try:
                if request.POST.get('comment') is not None:
                    Comment.objects.create(
                        user = request.user,
                        item = item,
                        comment = request.POST.get('comment')
                    )

                    return redirect('item', pk=item.id)
            except:
                pass

    context = {'item': item, 'highest_price_bid': highest_price_bid, 'categories': categories, 'artists': artists, 'numeber_of_bids': numeber_of_bids,
               'comments': comments, 'comments_count': comments_count}
    return render(request, 'base\\item.html', context)

def login_page(request):
    page = 'login'
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username = username)
        except:
            messages.error(request, "User doesn't exist")

        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Incorrect Password!")

    context = {'page': page}

    return render(request, 'base/login_register.html', context)

def logout_user(request):
    logout(request)
    return redirect('home')

def register_page(request):
    form = MyUserCreationForm
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Error')
    return render(request, 'base/login_register.html', {'form': form})

def user_profile(request,pk):
    user = User.objects.get(id=pk)
    categories = Category.objects.all()
    artists = User.objects.filter(is_artist=True)
    items = user.item_set.all()
    collection = Collection.objects.filter(owner__id=int(pk))


    context = {'user':user, 'categories':categories, 'artists':artists, 'items': items, 'collection': collection}
    return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def update_user(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES,  instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'base/update_user.html', {"form": form})


@login_required(login_url='login')
def create_item(request):
    form = ItemForm()
    categories = Category.objects.all()
    if request.method == 'POST':
        try:
            uploaded_picture = request.FILES['picture']
            fs = FileSystemStorage()
            fs.save(uploaded_picture.name, uploaded_picture)
            print(uploaded_picture)
        except:
            uploaded_picture = None

        if uploaded_picture is None:
            category_name = request.POST.get('category')
            category, created = Category.objects.get_or_create(name=category_name)
            item = Item.objects.create(
                artist = request.user,
                category = category,
                name = request.POST.get('name'),
                description=request.POST.get('description'),
                price =  request.POST.get('price')
            )
        else:
            category_name = request.POST.get('category')
            category, created = Category.objects.get_or_create(name=category_name)
            item = Item.objects.create(
                artist=request.user,
                category=category,
                name=request.POST.get('name'),
                description=request.POST.get('description'),
                price=request.POST.get('price'),
                picture = uploaded_picture
            )


        return redirect('home')


    context = {'form': form, 'categories': categories}
    return render(request, 'base/item_form.html', context)

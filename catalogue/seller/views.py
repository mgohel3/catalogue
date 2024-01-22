# seller/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Seller, Shop, Product, Banner, Category
from .forms import SellerRegistrationForm, SellerProfileForm, ShopForm, ShopEditForm, BannerUploadForm, CategoryForm, CategoryEditForm # Add ShopForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse
from django.core.paginator import Paginator
from .forms import ProductUploadForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q


def home(request):
    show_header_and_footer = True
    page_title = 'Home'
    return render(request, 'seller/home.html',{'show_header_and_footer': show_header_and_footer})

def seller_registration(request):
    show_header_and_footer = False

    if request.method == 'POST':
        form = SellerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # This saves the User instance
            seller = Seller.objects.create(
                user=user,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                phone_number=form.cleaned_data['phone_number'],
            )

            # Redirect to the seller dashboard after successful registration
            return redirect('seller:dashboard')
    else:
        form = SellerRegistrationForm()

    return render(request, 'seller/registration.html', {'form': form, 'show_header_and_footer': show_header_and_footer})


def seller_login(request):
    is_login_page = True  # Add this variable to indicate the login page
    show_header_and_footer = False
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, ("You are Logged in as " + username + "."))
                # Redirect to the seller dashboard after successful login
                return redirect('seller:dashboard')
            else:
                messages.error(request, 'Invalid login credentials.')
    else:
        form = AuthenticationForm()
    return render(request, 'seller/login.html', {'form': form, 'is_login_page': is_login_page,'show_header_and_footer': show_header_and_footer})

def seller_logout(request):
    logout(request)
    messages.success(request, ("You are Logged out"))
    return redirect('seller:login')


@login_required
def seller_dashboard(request):
    show_header_and_footer = False

    try:
        seller = request.user.seller
        shop = seller.shop
    except Seller.DoesNotExist:
        # If the user is not a seller, redirect them to the seller registration page
        messages.error(request, 'You are not registered as a seller. Please sign up as a seller.')
        return redirect('seller_signup')  # Update to the actual URL for seller registration

    return render(request, 'seller/dashboard.html', {'show_header_and_footer': show_header_and_footer, 'shop': shop})

@login_required
def seller_profile(request):
    try:
        seller = Seller.objects.get(user=request.user)
    except Seller.DoesNotExist:
        if request.method == 'POST':
            form = SellerProfileForm(request.POST)
            if form.is_valid():
                form.save()
                # Optionally, you can add a success message here
                return redirect('seller:profile')
        else:
            form = SellerProfileForm()

        return render(request, 'seller/profile.html', {'form': form})

    if request.method == 'POST':
        form = SellerProfileForm(request.POST, instance=seller)
        if form.is_valid():
            form.save()
            # Optionally, you can add a success message here
            return redirect('seller:profile')
    else:
        form = SellerProfileForm(instance=seller)

    return render(request, 'seller/profile.html', {'form': form})

def features(request):
    show_header_and_footer = True
    page_title = 'features'
    return render(request, 'seller/features.html',{'show_header_and_footer': show_header_and_footer})

def solutions(request):
    show_header_and_footer = True
    page_title = 'solutions'
    return render(request, 'seller/solutions.html',{'show_header_and_footer': show_header_and_footer})


from django.shortcuts import render


def all_product(request, business_name=None):
    show_header_and_footer = bool(business_name)

    # Fetch all products from the database
    all_products = Product.objects.filter(shop=request.user.seller.shop)

    # Get the list of categories and pass it to the template
    categories = Category.objects.filter(shop=request.user.seller.shop)

    # Assuming you want to filter products based on a selected category
    selected_category = request.GET.get('category')
    if selected_category:
        all_products = all_products.filter(
            Q(category__id=selected_category) | Q(category__parent_category__id=selected_category))

    page_title = 'All Products'

    return render(request, 'seller/all_product.html', {
        'show_header_and_footer': show_header_and_footer,
        'business_name': business_name,  # Pass the business_name to the template
        'page_title': page_title,
        'all_products': all_products,  # Pass all products to the template
        'categories': categories,  # Pass categories to the template
        'selected_category': selected_category,  # Pass selected category to the template
    })

def pricing(request):
    show_header_and_footer = True
    page_title = 'Pricing'
    return render(request, 'seller/pricing.html',{'show_header_and_footer': show_header_and_footer})

def sidebar(request):
    show_header_and_footer = False
    page_title = ''
    return render(request, 'seller/sidebar.html',{'show_header_and_footer': show_header_and_footer})

def settings(request):
    show_header_and_footer = False
    page_title = ''
    return render(request, 'seller/settings.html',{'show_header_and_footer': show_header_and_footer})

def settings_plan(request):
    show_header_and_footer = False
    page_title = ''
    return render(request, 'seller/settings_plan.html',{'show_header_and_footer': show_header_and_footer})

@login_required
def create_shop(request):
    # Check if the user already has a shop
    existing_shop = request.user.seller.shop
    if existing_shop:
        # Redirect to the existing shop
        return redirect('seller:shop_page', business_name=existing_shop.name)

    if request.method == 'POST':
        form = ShopForm(request.POST, request.FILES)
        if form.is_valid():
            shop = form.save(commit=False)
            shop.user = request.user
            shop.save()

            # Ensure the shop is associated with the currently logged-in user's seller profile
            seller_profile = request.user.seller
            seller_profile.shop = shop
            seller_profile.save()

            return redirect('seller:shop_page', business_name=shop.name)
    else:
        form = ShopForm()

    return render(request, 'seller/create_shop.html', {'form': form})

def edit_shop(request, business_name):
    # Retrieve the shop using the business_name
    shop = get_object_or_404(Shop, name=business_name)

    if request.method == 'POST':
        form = ShopEditForm(request.POST, request.FILES, instance=shop)
        if form.is_valid():
            form.save()
    else:
        form = ShopEditForm(instance=shop)

    return render(request, 'seller/edit_shop.html', {'form': form, 'shop': shop})

def shop_page(request, business_name):
    shop = get_object_or_404(Shop, name=business_name)
    products = Product.objects.filter(shop=shop)  # Assuming a reverse relation from Shop to Product
    banners = Banner.objects.filter(shop=shop)  # Fetch banners for the specific shop
    return render(request, 'seller/shop_page.html', {'shop': shop, 'products': products,'banners': banners})


@login_required
def add_product(request):
    if request.user.seller.shop:
        if request.method == 'POST':
            form = ProductUploadForm(request.POST, request.FILES)
            if form.is_valid():
                product = form.save(commit=False)
                product.shop = request.user.seller.shop
                product.save()

                # Generate the URL for the 'shop_page' view with the business_name parameter
                shop_page_url = reverse('seller:shop_page', kwargs={'business_name': request.user.seller.shop.name})

                return redirect('seller:all_product')
        else:
            form = ProductUploadForm()

        return render(request, 'seller/add_product.html', {'form': form})
    else:
        return redirect('seller:all_product')
@login_required
def edit_product(request, product_id):
    if request.user.seller.shop:
        # Fetch the product instance from the database
        product = get_object_or_404(Product, id=product_id)
        category = Category.objects.all()  # Fetch all existing categories

        # Check if the logged-in user owns the shop associated with the product
        if product.shop == request.user.seller.shop:
            if request.method == 'POST':
                # Populate the form with the current product instance and the posted data
                form = ProductUploadForm(request.POST, request.FILES, instance=product)
                if form.is_valid():
                    form.save()
                    # Redirect to the shop page after successful update
                    shop_page_url = reverse('seller:all_product')
                    return redirect(shop_page_url)
            else:
                # Populate the form with the current product instance for editing
                form = ProductUploadForm(instance=product)

            return render(request, 'seller/edit_product.html', {'form': form, 'product': product})
        else:
            # If the user doesn't own the shop, you can handle it as needed (e.g., show an error page)
            return render(request, 'seller/error.html', {'error_message': 'You do not have permission to edit this product.'})
    else:
        return redirect('seller:all_product')

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    shop = product.shop
    return render(request, 'seller/product.html', { 'product': product, 'shop': shop} )
def delete_product(request, product_id):
    if request.user.seller.shop:
        # Fetch the product instance from the database
        product = get_object_or_404(Product, id=product_id)

        # Check if the logged-in user owns the shop associated with the product
        if product.shop == request.user.seller.shop:
            # Delete the product from the database
            product.delete()

            # Redirect to the shop page after successful deletion
            shop_page_url = reverse('seller:all_product')
            return redirect(shop_page_url)
        else:
            # If the user doesn't own the shop, you can handle it as needed (e.g., show an error page)
            return render(request, 'seller/error.html', {'error_message': 'You do not have permission to delete this product.'})
    else:
        return redirect('seller:all_product')


@login_required
def add_banner(request):
    if request.method == 'POST':
        banner_form = BannerUploadForm(request.POST, request.FILES)
        if banner_form.is_valid():
            # Create a new Banner instance and associate it with the logged-in seller's shop
            banner_instance = banner_form.save(commit=False)

            # Ensure the shop is associated with the currently logged-in user's seller profile
            banner_instance.shop = request.user.seller.shop

            banner_instance.save()

            return redirect('seller:all_banners')  # Redirect to the dashboard or another page after successful upload
    else:
        banner_form = BannerUploadForm()

    return render(request, 'seller/add_banner.html', {'banner_form': banner_form})

def show_banners(request):
    banners = Banner.objects.all()
    return render(request, 'seller/show_banners.html', {'banners': banners})

def all_banners(request):
    # Fetch all banners from the database
    all_banners = Banner.objects.filter(shop=request.user.seller.shop)

    # Assuming you have a template named 'seller/all_banners.html'
    return render(request, 'seller/all_banners.html', {'all_banners': all_banners})

def delete_banner(request, banner_id):
    if request.user.seller.shop:
        # Fetch the banner instance from the database
        banner = get_object_or_404(Banner, id=banner_id)

        # Check if the logged-in user owns the shop associated with the banner
        if banner.shop == request.user.seller.shop:
            # Delete the banner from the database
            banner.delete()

            # Redirect to the dashboard or another page after successful deletion
            messages.success(request, 'Banner deleted successfully.')
            return redirect('seller:all_banners')
        else:
            # If the user doesn't own the shop, you can handle it as needed (e.g., show an error page)
            return render(request, 'seller/error.html', {'error_message': 'You do not have permission to delete this banner.'})
    else:
        return redirect('seller:all_banners')


@login_required
def add_category(request):
    show_header_and_footer = False

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)

            # Ensure the category is associated with the currently logged-in user's seller profile
            category.shop = request.user.seller.shop

            category.save()

            # Redirect to the category list page after successful category creation
            return redirect(reverse('seller:all_category'))
    else:
        form = CategoryForm()

    return render(request, 'seller/add_category.html', {'form': form, 'show_header_and_footer': show_header_and_footer})

@login_required
def all_category(request):
    # Fetch all categories associated with the currently logged-in user's shop
    all_categories = Category.objects.filter(shop=request.user.seller.shop)
    return render(request, 'seller/all_category.html', {'all_categories': all_categories})

@login_required
def edit_category(request, category_id):
    # Fetch the category instance from the database
    category = get_object_or_404(Category, id=category_id)

    # Check if the logged-in user owns the shop associated with the category
    if request.user.seller.shop == category.shop:
        if request.method == 'POST':
            form = CategoryEditForm(request.POST, instance=category)
            if form.is_valid():
                form.save()
                # Redirect to the category list page after successful category edit
                return redirect('seller:all_category')
        else:
            form = CategoryEditForm(instance=category)

        return render(request, 'seller/edit_category.html', {'form': form, 'category': category})
    else:
        # If the user doesn't own the shop, you can handle it as needed (e.g., show an error page)
        return render(request, 'seller/error.html',
                      {'error_message': 'You do not have permission to edit this category.'})

@login_required
def delete_category(request, category_id):
    # Fetch the category instance from the database
    category = get_object_or_404(Category, id=category_id)

    # Check if the logged-in user owns the shop associated with the category
    if request.user.seller.shop == category.shop:
        # Delete the category from the database
        category.delete()

        # Redirect to the dashboard or another page after successful deletion
        messages.success(request, 'Category deleted successfully.')
        return redirect('seller:all_category')
    else:
        # If the user doesn't own the shop, you can handle it as needed (e.g., show an error page)
        return render(request, 'seller/error.html',
                      {'error_message': 'You do not have permission to delete this category.'})


from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login


# views.py is called from urls.py. Individual url mappings
# are mapping to specific functions, which display
# and render templates accordingly.

# View for the index / or /rango page.
def index(request):
	category_list = Category.objects.order_by('-likes')[:5]
	pages_list = Page.objects.order_by('-views')[:5]
	context_dict = {'categories': category_list, 'pages': pages_list}
	sdff = reverse('index')
	return render(request, 'rango/index.html', context=context_dict)

# View for the /about page.
def about(request):
	return render(request, 'rango/about.html', {})

# View for showing the category pages
def show_category(request, category_name_slug):
	context_dict = {}

	try:
		category = Category.objects.get(slug = category_name_slug)
		pages = Page.objects.filter(category = category)
		context_dict['pages'] = pages
		context_dict['category'] = category
	except Category.DoesNotExist:
		context_dict['category'] = None
		context_dict['pages'] = None

	return render(request, 'rango/category.html', context_dict)

# View for adding a category
def add_category(request):
	form = CategoryForm()

	if request.method == 'POST':
		form = CategoryForm(request.POST)

		if form.is_valid():
			form.save(commit = True)
			return index(request)
		else:
			print(form.errors)

	return render(request, 'rango/add_category.html', {'form': form})

# View for adding a page
def add_page(request, category_name_slug):
	try:
		category = Category.objects.get(slug=category_name_slug)
	except Category.DoesNotExist:
		category = None

	form = PageForm()

	if request.method == 'POST':
		form = PageForm(request.POST)

		if form.is_valid():
			if category:
				page = form.save(commit = False)
				page.category = category
				page.views = 0
				page.save()
				return show_category(request, category_name_slug)
		else:
			print(form.errors)

	context_dict = {'form': form, 'category': category}
	return render(request, 'rango/add_page.html', context_dict)

def register(request):
	registered = False

	if request.method == 'POST':
		user_form = UserForm(data = request.POST)
		profile_form = UserProfileForm(data = request.POST)

		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()

			user.set_password(user.password)
			user.save()

			profile = profile_form.save(commit = False)
			profile.user = user

			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']

			profile.save()

			registered = True
		else:
			print(user_form.errors, profile_form.errors)
	else:
		user_form = UserForm()
		profile_form = UserProfileForm()

	context_dict = {'user_form': user_form, 'profile_form': profile_form, 'registered': registered}
	return render(request, 'rango/register.html', context = context_dict)

def user_login(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(username = username, password = password)

		if user:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect(reverse('rango:index'))
			else:
				return HttpResponse('Your Rango account is disabled.')
		else:
			print ("Invalid login details: {0}, {1}".format(username, password))
			return HttpResponse("Invalid login details supplied.")

	else:
		return render(request, 'rango/login.html', {})

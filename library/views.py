# Create your views here.
from accounts.models import Admin, Student
from library.forms import order_details_form,books_inventory_form,update_inventory_form
from django.shortcuts import render, redirect
from django.urls import path
from django.http import HttpResponse
from datetime import timedelta
from django.utils import timezone
from django.views.generic import CreateView
from .models import Inventory, Payment_bill, Books, Seller, Seller_inventory, College
from django import forms


# Create your views here.
# -----------------------------------------------------------------------------------------------------------
# function that dispalys all the transactions made in a time period,
# default is previous week
# for now it just prints all the transactions made
# this function automatically adds a row whenever an order is placed
def payment_details(request):
    user = request.user
    admin = Admin.objects.get(user=user)
    payments = Payment_bill.objects.filter(college=admin.college).order_by('-time_of_transaction')[:100]
    context = {'payments': payments}
    return render(request, '../templates/payment_details.html', context)
# --------------------------------------------------------------------------------------------------------




# print all student of a particular college





# --------------------------------------------------------------------------------------------------------
# functions that display the list of sellers who can accomodate the book order
# and their net prices
def enter_order_specs(request):
    user = request.user
    if request.method == 'POST':
        form = order_details_form(request.POST)
        if form.is_valid():
            # getting details of the values from the form
            request.session['Book_id'] = form.cleaned_data['Book_id']
            request.session['Book_name'] = form.cleaned_data['Book_name']
            request.session['Quantity'] = form.cleaned_data['Quantity']
            #request.session['Price_points'] = form.cleaned_data['Price_points']
            # request.session['College_id'] = form.cleaned_data['College_id']

            return redirect('/library/place_order')

        else:
            form = order_details_form()
    return render(request, '../templates/enter_order_specs.html', {'form': order_details_form(request.POST)})

def place_order(request):
    user = request.user
    available_sellers = Seller_inventory.objects.filter(book__Book_id__exact=request.session['Book_id'],
                                                            book_count__gte=request.session['Quantity']).order_by(
        'seller__Shipping_cost')
    context = {'available_sellers': available_sellers}
    # on the same page we will display a table with buttons
    # as options to select the sellers who can accomodate the order.
    admin = Admin.objects.get(user=user)
    admin_college = admin.college
    if (request.POST):
        seller_id = request.POST.get('seller_opt_radio')
        if (seller_id != None):
            seller = Seller.objects.get(Seller_id=seller_id)
            # need to add the books quantity to the database inventory
            # if the book is already in inventory update its Book_count
            if (Inventory.objects.filter(Books__Book_id__exact=request.session['Book_id'],
                                             College=admin_college).exists()):
                already_existing_book = Books.objects.get(Book_id__exact=request.session['Book_id'])
                inv_obj = Inventory.objects.get(Books__Book_id__exact=request.session['Book_id'],
                                                    College=admin_college)
                inv_obj.Book_count = inv_obj.Book_count + request.session['Quantity']
                inv_obj.save()

                cost_of_purchase = seller.Shipping_cost + (
                        request.session['Quantity'] * already_existing_book.Price_points * 5)
                payment = Payment_bill(cost=cost_of_purchase, book=already_existing_book, seller=seller,
                                           college=admin_college)
                payment.save()
                # if the book is not in inventory create a new book and set it Book_count
            else:
                new_book = Books.objects.get(Book_id__exact=request.session['Book_id'])
                inv_obj = Inventory(College=admin_college, Books=new_book, Book_count=request.session['Quantity'])
                inv_obj.save()

                cost_of_purchase = seller.Shipping_cost + (
                        request.session['Quantity'] * new_book.Price_points * 5)
                payment = Payment_bill(
                    cost=cost_of_purchase, book=new_book, seller=seller, college=admin_college)
                payment.save()

                # if we want the seller's inventory to be managed as well we could do this in
                # seller_inv = seller_inventory.objects.get(Book_id__exact=request.session['Book_id'])
        # redirecting to the admin home url
        return redirect('/library/payment_details')

    return render(request, '../templates/place_order.html', context)

    # dealing with redirections etc. from the admin home page.

def redirect_to_enter_order_specs(request):
    return redirect('/library/enter_order_specs')
    
'''def enter_college_id(request):
	user = request.user
	if request.method == 'POST':
		form = books_inventory_form(request.POST)
		if form.is_valid():
			request.session['College_id'] = form.cleaned_data['College_id']
			return redirect('/library/show_books')

		else:
			form = books_inventory_form()

	return render(request, '../templates/BooksInventory.html', {'form': books_inventory_form(request.POST)})'''

    # given the college id
    # i am getting all the books in that college's inventory

def show_books(request):
	user = request.user
	admin = Admin.objects.filter(user=user)
	college = admin[0].college
	intv = Inventory.objects.filter(College=college)
	books_list = Inventory.objects.filter(College=college).values_list('Books',flat=True)
	books = Books.objects.filter(Book_id__in=books_list)
	context = {'books': intv}
	return render(request, '../templates/BooksInventory.html', context)

def upd_inventory(request):
	user = request.user
	admin = Admin.objects.filter(user=user)
	college = admin[0].college
	if request.method == 'POST':
		form = update_inventory_form(request.POST)
		if form.is_valid():
			bid = form.cleaned_data['Book_id']
			bname = form.cleaned_data['Book_name']
			bpub = form.cleaned_data['Publisher']
			bauth = form.cleaned_data['Author']
			btype = form.cleaned_data['Book_type']
			bpp = form.cleaned_data['Price_points']
			bquan = form.cleaned_data['Quantity']

			if(Inventory.objects.filter(Books__Book_id__exact=bid,College=college).exists()):
				already_existing_book = Books.objects.get(Book_id__exact=bid)
				inv_obj = Inventory.objects.get(Books__Book_id__exact= bid, College=college)
				inv_obj.Book_count = inv_obj.Book_count + bquan
				inv_obj.save()
				return redirect('/accounts/admin_home')


			else:
				'''books_2=Books.objects.get(Book_id__exact=bid)
				inv_obj2=Inventory(Books__Book_id=bid,
					Books__Book_name=bname,Books__Publisher=bpub,
					Books__Author=bauth,Books__Book_type=request.session['Book_type'],
					Books__Price_points=bpp,College=college,Book_count=bquan)'''

				#inv_obj2.save()
				new_book = Books.objects.get(Book_id__exact=bid)
				inv_obj = Inventory(College=college, Books= new_book, Book_count= bquan)
				inv_obj.save()
				return redirect('/accounts/admin_home')



	else:
		form = update_inventory_form()


	return render(request, '../templates/UpdateInventory.html', {'form': update_inventory_form(request.POST)})
def print_college_users(request):
    user = request.user
    admin = Admin.objects.filter(user=user)
    college = admin[0].college
    college1 = College.objects.get(College_id = college.College_id)
    student = Student.objects.filter(College__exact = college1).order_by('student_id')
    context = {'student': student}
    return render(request, '../templates/college_users.html', context)

	







    
    
    
    

	
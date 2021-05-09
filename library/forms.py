from django import forms

# this is a form to import all details of an order from the admin

class order_details_form(forms.Form):
    Book_name = forms.CharField(max_length=255, required=True)
    Book_id = forms.CharField(max_length=255, required=True)
    Quantity = forms.IntegerField(required=True)
    # not sure if this is needed or not
    #Price_points = forms.IntegerField(required=True)

# this is a form to import the college id to show all the books in the inventory of that college

class books_inventory_form(forms.Form):
    College_id = forms.CharField(max_length=255, required=True)

class update_inventory_form(forms.Form):
    Book_id = forms.CharField(max_length=255, required=True, label="Book ID",widget=forms.TextInput(attrs={'placeholder':'Book ID'}))
    Book_name = forms.CharField(max_length=255, required=True, label="Book name",widget=forms.TextInput(attrs={'placeholder':'Book name'}))
    Publisher = forms.CharField(max_length=255, required=True,widget=forms.TextInput(attrs={'placeholder':'Publisher'}))
    Author = forms.CharField(max_length=255, required=True,widget=forms.TextInput(attrs={'placeholder':'Author'}))
    Book_type = forms.CharField(max_length=255, required=True, label="Book type",widget=forms.TextInput(attrs={'placeholder':'Book type'}))
    Price_points = forms.IntegerField(required=True,label="Price points",widget=forms.TextInput(attrs={'placeholder':'Price points'}))
    Quantity = forms.IntegerField(required=True,widget=forms.TextInput(attrs={'placeholder':'Quantity'}))
    
    
    
    
    



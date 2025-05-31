from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404, render, redirect
from .models import Item


def item_list(request):
   items = Item.objects.all()
   return render(request, 'store/item_list.html', {'items': items})


def add_to_cart(request, item_id):
   item = get_object_or_404(Item, id=item_id)
   cart = request.session.get('cart', [])
   # Prevent duplicates
   if not any(i['id'] == item.id for i in cart):
      cart.append({
         'id': item.id,
         'name': item.name,
         'description': item.description,
         'price': float(item.price),
         'category': item.category,
         'image_url': item.image.url if item.image else '',
      })
      request.session['cart'] = cart
   return redirect('item_list')


def checkout(request):
   cart = request.session.get('cart', [])
   return render(request, 'checkout.html', {'items': cart})


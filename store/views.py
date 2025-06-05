# Create your views here.
from decimal import Decimal
from django.http import JsonResponse
from .models import Item, Order, OrderItem, Category
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, render, redirect

###################################################

def item_list(request):
   selected_category = request.GET.get('category')
   categories = Category.objects.all()

   if selected_category:
      items = Item.objects.filter(category__name=selected_category)
   else:
      items = Item.objects.all()

   cart = request.session.get('cart', [])
   cart_item_ids = [item['id'] for item in cart]  # ✅ Fixed this line

   return render(request, 'item_list.html', {
      'items': items,
      'categories': categories,
      'selected_category': selected_category,
      'cart_item_ids': cart_item_ids,
   })


###################################################

def add_to_cart(request, item_id):
   item = get_object_or_404(Item, id=item_id)
   cart = request.session.get('cart', [])

   for i in cart:
      if i['id'] == item.id:
         # Already in cart, don’t add again
         return redirect('item_list')

   cart.append({
      'id': item.id,
      'name': item.name,
      'description': item.description,
      'price': float(item.price),
      'category': item.category.id,
      'image_url': item.image.url if item.image else '',
      'quantity': 1,  # ✅ default to 1
   })

   request.session['cart'] = cart
   return redirect('item_list')

###################################################

def checkout(request):
   cart = request.session.get('cart', [])
   total = sum(item['price'] * item['quantity'] for item in cart)
   return render(request, 'checkout.html', {
      'items': cart,
      'total': total
   })

###################################################

def about_us(request):
   return render(request, 'about_us.html')

###################################################

def disclaimer(request):
   return render(request, 'disclaimer.html')

###################################################

def privacy(request):
   return render(request, 'privacy.html')

###################################################

def terms(request):
   return render(request, 'terms.html')

###################################################

def order_success(request):
   return render(request, 'order_success.html')

###################################################

def contact_us(request):
   return render(request, 'contact_us.html')

###################################################

@require_POST
def place_order(request):
   cart = request.session.get('cart', [])

   if not cart:
      return redirect('checkout')

   order = Order.objects.create()

   for item in cart:
      OrderItem.objects.create(
         order=order,
         name=item['name'],
         description=item['description'],
         price=item['price'],
         quantity=item['quantity'],
         category=item['category'],
         image_url=item['image_url'],
         sub_total=item['price']*item['quantity']
      )

   # Track order data
   total_amount = create_order_from_cart(cart).total_amount

   # Clear the cart
   request.session['cart'] = []
   return render(request, 'payment.html', {'order': order, 'total_amount': total_amount})
   #return render(request, 'order_success.html', {'order': order, 'total_amount': total_amount})

###################################################

def update_cart(request):
   if request.method == 'POST':
      item_id = request.POST.get('item_id')
      action = request.POST.get('action')

      cart = request.session.get('cart', [])

      updated_item = None  # Track the specific item

      for item in cart:
         if str(item['id']) == str(item_id):
            if action == 'increase':
               item['quantity'] += 1
            elif action == 'decrease' and item['quantity'] > 1:
               item['quantity'] -= 1
            updated_item = item  # Save the matched item
            break

      request.session['cart'] = cart

      if not updated_item:
         return JsonResponse({'success': False, 'error': 'Item not found'}, status=404)

      item_total = updated_item['quantity'] * updated_item['price']
      cart_total = sum(i['quantity'] * i['price'] for i in cart)

      return JsonResponse({
         'success': True,
         'item_id': updated_item['id'],
         'item_quantity': updated_item['quantity'],
         'item_total': item_total,
         'cart_total': cart_total,
      })

   return JsonResponse({'success': False}, status=400)



###################################################

def create_order_from_cart(cart):
   """
      cart = [
         {"name": "Banana", "quantity": 2, "price": 18.0},
         {"name": "Apple", "quantity": 1, "price": 30.0},
      ]
   """
   
   summary_lines = []
   total_amount = Decimal('0.00')

   for item in cart:
      sub_total = Decimal(item['price']) * item['quantity']
      line = f"{item['quantity']} {item['name']} (${sub_total})"
      summary_lines.append(line)
      total_amount += sub_total

   summary = ", ".join(summary_lines)

   # Save the order
   order = Order.objects.create(summary=summary, total_amount=total_amount)
   return order


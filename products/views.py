# ==============================
# IMPORTS
# ==============================

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from .models import Product, Order, OrderItem

from django.shortcuts import render, get_object_or_404
from .models import Product
from .models import Order

from .forms import CheckoutForm
from .models import Product, Order, OrderItem
from django.shortcuts import render, redirect
from .models import ContactMessage
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import send_mail





# ==============================
# BASIC PAGES
# ==============================

def home(request):
    """Homepage"""
    return render(request, "products/home.html")


def about(request):
    """About page"""
    return render(request, "products/about.html")




def contact(request):
    print("CONTACT VIEW ACTIVE")
    if request.method == "POST":

        # get form data
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        message_text = request.POST.get("message")

        # ✅ SAVE MESSAGE TO DATABASE
        contact = ContactMessage.objects.create(
            name=name,
            email=email,
            phone=phone,
            message=message_text
        )

        # ✅ AUTO EMAIL REPLY
        print("EMAIL BLOCK REACHED")
        send_mail(
            subject="We received your message — Samprathi",
            message="""
Thank you for contacting Samprathi.

We have received your message and will reply shortly.

For faster response, please contact us via WhatsApp.

— Team Samprathi
""",
            from_email="noreply@samprathi.com",
            recipient_list=[email],
            fail_silently=False,
        )

        messages.success(request, "Message sent successfully!")

        return redirect("contact")

    return render(request, "products/contact.html")


# ==============================
# PRODUCT VIEWS
# ==============================

def product_list(request):
    """Display all available products"""
    products = Product.objects.filter(available=True)
    return render(request, "products/product_list.html", {
        "products": products
    })


def shop(request):
    """Shop page (same as product list but different template)"""
    products = Product.objects.filter(available=True)
    return render(request, "products/shop.html", {
        "products": products
    })


def product_detail(request, id):
    """Single product details"""
    product = get_object_or_404(Product, id=id)

    return render(request, "products/product_detail.html", {
        "product": product
    })


# ==============================
# CART FUNCTIONS (SESSION CART)
# ==============================

def add_to_cart(request, id):
    """Add product to session cart"""
    product = get_object_or_404(Product, id=id)

    cart = request.session.get("cart", {})

    if str(id) in cart:
        cart[str(id)] += 1
    else:
        cart[str(id)] = 1

    request.session["cart"] = cart
    request.session.modified = True

    return redirect("cart")



def cart(request):

    cart = request.session.get('cart', {})

    products = []
    total = 0

    for product_id, qty in cart.items():
        product = get_object_or_404(Product, id=product_id)

        subtotal = product.price * qty
        total += subtotal

        products.append({
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "qty": qty,
            "subtotal": subtotal,
        })

    return render(request, "products/cart.html", {
        "products": products,
        "total": total
    })


def remove_from_cart(request, id):
    """Remove item completely from cart"""
    cart = request.session.get("cart", {})

    if str(id) in cart:
        del cart[str(id)]

    request.session["cart"] = cart
    return redirect("cart")


def update_cart(request, id, action):
    """Increase or decrease product quantity"""
    cart = request.session.get("cart", {})
    product_id = str(id)

    if product_id in cart:

        if action == "increase":
            cart[product_id] += 1

        elif action == "decrease":
            cart[product_id] -= 1

            if cart[product_id] <= 0:
                del cart[product_id]

    request.session["cart"] = cart
    return redirect("cart")


# ==============================
# USER AUTHENTICATION
# ==============================

def register(request):
    """User registration"""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()

    return render(request, "products/register.html", {
        "form": form
    })


# ==============================
# CHECKOUT & ORDERS
# ==============================


@login_required
def checkout(request):

    cart = request.session.get('cart', {})

    products = []
    total = 0

    for product_id, qty in cart.items():
        product = Product.objects.get(id=product_id)
        subtotal = product.price * qty

        products.append({
            "product": product,
            "qty": qty,
            "subtotal": subtotal
        })

        total += subtotal

    if request.method == "POST":
        form = CheckoutForm(request.POST)

        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_price = total
            order.save()

            # create order items + reduce stock
            for item in products:

                product = item["product"]
                qty = item["qty"]

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=qty,
                    price=product.price
                )

                # reduce stock
                product.stock -= qty

                if product.stock <= 0:
                    product.stock = 0
                    product.available = False

                product.save()

            # clear cart
            request.session['cart'] = {}

            return redirect('order_success')

    else:
        form = CheckoutForm()

    return render(request, "products/checkout.html", {
        "form": form,
        "products": products,
        "total": total
    })




@login_required
def order_success(request):
    """Order success page"""
    return render(request, "products/order_success.html")


def my_orders(request):
    # Later: show user's orders
    return render(request, 'products/my_orders.html', {}) 

 

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'orders': orders,
        'title': 'My Orders - Samprathi',
    }
    return render(request, 'products/my_orders.html', context)



def tracking(request):
    order = None

    if request.method == "POST":
        order_id = request.POST.get("order_id")
        if order_id:
            order = Order.objects.filter(id=order_id).first()

    return render(request, "products/tracking.html", {
        "order": order
    })   

def faq(request):
    return render(request, "products/faq.html")



@staff_member_required
def inquiries(request):
    messages = ContactMessage.objects.all().order_by('-created_at')

    return render(request, "products/inquiries.html", {
        "messages": messages
    })

from django.shortcuts import get_object_or_404, redirect

@staff_member_required
def mark_replied(request, id):
    message = get_object_or_404(ContactMessage, id=id)
    message.replied = True
    message.save()
    return redirect('inquiries')
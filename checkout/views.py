from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.conf import settings
from works.models import Product
from profiles.models import UserProfile
from profiles.forms import UserProfileForm
from .models import OrderItem, Order
from .forms import OrderForm
from works.context_processors import bookcart_contents
import stripe
from .email_confirmation import send_confirmation_email


def checkout(request):
    """
    Handle the checkout process for a user's bookcart.

    Processes both GET and POST requests. For GET requests, displays the
    checkout form and sets up Stripe payment. For POST requests, validates
    the order form, creates the order, and processes the payment.
    """
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        bookcart = request.session.get(
            'bookcart', {}
        )

        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'billing_address1': request.POST['billing_address1'],
            'billing_address2': request.POST['billing_address2'],
            'billing_city': request.POST['billing_city'],
            'billing_postcode': request.POST['billing_postcode'],
            'billing_country': request.POST['billing_country'],
        }

        order_form = OrderForm(form_data)
        if order_form.is_valid():
            try:
                order = order_form.save(commit=False)
                if request.user.is_authenticated:
                    order.user = request.user
                order.payment_status = 'paid'
                order.save()

                # Create order items
                for item_id, quantity in bookcart.items():
                    try:
                        product = Product.objects.get(pk=item_id)
                        if isinstance(quantity, list):
                            quantity = sum(quantity)

                        OrderItem.objects.create(
                            order=order,
                            product=product,
                            quantity=quantity,
                            price=product.price
                        )
                    except Product.DoesNotExist:
                        messages.error(request, "Product not found.")
                        order.delete()
                        return redirect(reverse('view_bookcart'))

                # Handle authenticated user profile
                if request.user.is_authenticated:
                    try:
                        profile = UserProfile.objects.get(user=request.user)
                        order.user_profile = profile
                        order.save()

                        # Calculate and save total
                        total = sum(
                            item.product.price * item.quantity
                            for item in order.orderitem_set.all()
                        )
                        order.total_amount = total
                        order.save()

                        if 'save-info' in request.POST:
                            request.session['save_info'] = True

                        # Send confirmation email
                        try:
                            send_confirmation_email(order)
                        except Exception as e:
                            messages.error(
                                request, f'Confirmation email not sent: {e}'
                            )

                        return redirect(reverse(
                            'checkout_success', args=[order.id]))
                    except UserProfile.DoesNotExist:
                        messages.error(request, 'Profile not found.')
                        return redirect(reverse('view_bookcart'))

                # For non-authenticated users, send email nad redirect
                try:
                    send_confirmation_email(order)
                except Exception as e:
                    messages.error(
                        request, f'Confirmation email not sent: {e}'
                    )

                return redirect(reverse('checkout_success', args=[order.id]))

            except Exception as e:
                messages.error(
                    request, f'Error processing your order: {str(e)}'
                )
                return redirect(reverse('view_bookcart'))
        else:
            messages.error(request, f'Form errors: {order_form.errors}')
            return redirect(reverse('view_bookcart'))

    # GET request handling
    else:
        bookcart = request.session.get('bookcart', {})
        if not bookcart:
            messages.error(
                request, "You ain't having no books in your bookcart."
            )
            return redirect(reverse('all_works'))

        current_bookcart = bookcart_contents(request)
        total = current_bookcart['total']
        stripe_total = round(total * 100)

        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        # Pre-fill form for authenticated users
        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                initial_data = {
                    'full_name': profile.profile_full_name,
                    'email': profile.profile_email,
                    'phone_number': profile.profile_phone_number,
                    'billing_address1': profile.profile_address1,
                    'billing_address2': profile.profile_address2,
                    'billing_city': profile.profile_city,
                    'billing_postcode': profile.profile_postcode,
                    'billing_country': profile.profile_country,
                }
                order_form = OrderForm(initial=initial_data)
            except UserProfile.DoesNotExist:
                # If profile doesn't exist, create it
                UserProfile.objects.create(user=request.user)
                order_form = OrderForm()
        else:
            order_form = OrderForm()

    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
        'bookcart_items': current_bookcart['bookcart_items'],
        'total': total,
    }

    return render(request, 'checkout/checkout.html', context)


def checkout_success(request, order_id):
    """
    Handle successful checkouts and post-purchase processing.

    Updates order status, saves user profile information if requested,
    and cleans up the session bookcart.
    """
    order = get_object_or_404(Order, id=order_id)

    if order.payment_status == 'pending':
        order.payment_status = 'paid'
        order.save()

    total = sum(
        item.product.price * item.quantity
        for item in order.orderitem_set.all()
    )

    if request.user.is_authenticated:
        try:
            profile = request.user.profile
            # Save the user's info
            if 'save_info' in request.session:
                profile_data = {
                    'profile_full_name': order.full_name,
                    'profile_email': order.email,
                    'profile_phone_number': order.phone_number,
                    'profile_address1': order.billing_address1,
                    'profile_address2': order.billing_address2,
                    'profile_city': order.billing_city,
                    'profile_postcode': order.billing_postcode,
                    'profile_country': order.billing_country,
                }

                user_profile_form = UserProfileForm(
                    data=profile_data, instance=profile)
                if user_profile_form.is_valid():
                    user_profile_form.save()
                else:
                    messages.error(
                        request, 'There was an error with your form. '
                        'Please double check your information.'
                    )

        except UserProfile.DoesNotExist:
            messages.error(request, 'Profile not found.')

    if 'bookcart' in request.session:
        del request.session['bookcart']

    messages.success(request, f'Order successfully processed! \
        Your order number is {order_id}. A confirmation \
        email will be sent to {order.email}.')

    context = {
        'order': order,
        'total': total,
    }

    return render(request, 'checkout/checkout_success.html', context)

from django.test import TestCase
from django.contrib.auth import get_user_model
from checkout.models import Order, OrderItem
from works.models import Product
from profiles.models import UserProfile
from decimal import Decimal


class TestOrderModel(TestCase):
    def setUp(self):
        # Create a test user
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

        # Create a user profile
        self.profile = UserProfile.objects.get(user=self.user)

        # Create a test product
        self.product = Product.objects.create(
            name='Test Book',
            description='A test book description',
            price=Decimal('29.99')
        )

        # Create a basic order
        self.order = Order.objects.create(
            user=self.user,
            user_profile=self.profile,
            full_name='Test User',
            email='test@example.com',
            phone_number='1234567890',
            billing_address1='123 Test St',
            billing_city='Test City',
            billing_postcode='12345',
            billing_country='GB'
        )

    def test_order_creation(self):
        """Test that an order can be created with correct initial values"""
        self.assertEqual(self.order.payment_status, 'pending')
        self.assertEqual(self.order.total_amount, Decimal('0'))
        self.assertEqual(str(self.order), f'Order {self.order.id} - testuser')

    def test_order_update_total(self):
        """Test the update_total method correctly calculates order total"""
        # Create two order items
        OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
            price=self.product.price
        )
        OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=1,
            price=self.product.price
        )

        # Update total
        self.order.update_total()

        # Expected total: (2 * 29.99) + (1 * 29.99) = 89.97
        expected_total = Decimal('89.97')
        self.assertEqual(self.order.total_amount, expected_total)

    def test_order_items_creation(self):
        """Test that order items can be created and associated with an order"""
        order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=1,
            price=self.product.price
        )

        self.assertEqual(order_item.order, self.order)
        self.assertEqual(order_item.quantity, 1)
        self.assertEqual(order_item.price, self.product.price)

    def test_payment_status_update(self):
        """Test that payment status can be updated"""
        self.order.payment_status = 'paid'
        self.order.save()

        # Refresh from database
        updated_order = Order.objects.get(id=self.order.id)
        self.assertEqual(updated_order.payment_status, 'paid')

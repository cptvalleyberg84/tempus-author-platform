from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Category(models.Model):
    """
    Model representing product categories.
    """
    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=255)
    friendly_name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        """
        String representation of the Category model.
        """
        return self.friendly_name or self.name

    def get_friendly_name(self):
        """
        Get the user-friendly name for the category.
        """
        return self.friendly_name


class Product(models.Model):
    """
    Model representing products/works available for purchase.
    """
    category = models.ForeignKey(
        'Category', null=True, blank=True, on_delete=models.SET_NULL
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=9, decimal_places=2)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)

    def average_rating(self):
        """
        Calculate the average rating from approved reviews.
        """
        reviews = self.reviews.filter(approved=True)
        if reviews:
            return sum(review.rating for review in reviews) / len(reviews)
        return 0

    def __str__(self):
        """
        String representation of the Product model.
        """
        return self.name

    def get_absolute_url(self):
        """
        Get the URL for the product detail view.
        """
        return reverse('work_detail', kwargs={'work_id': self.id})


class Review(models.Model):
    """
    Model representing user reviews for products.

    Each user can only submit one review per product.
    Reviews must be approved before being displayed.
    """
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='reviews'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')],
        verbose_name="Rating (required)"
    )
    comment = models.TextField(
        blank=True, null=True, verbose_name="Review (optional)",
        help_text="Share your thought about this story (optional)."
    )
    created_date = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_date']
        unique_together = ('product', 'user')

    def __str__(self):
        """
        String representation of the Review model.
        """
        return f'{self.user.username} review for {self.product.name}'

from django.db import models
from django.utils import timezone


class CarouselItem(models.Model):
    """
    Model representing items in the homepage carousel.
    """

    STYLE_CHOICES = [
        ('product', 'Product Style'),
        ('blog', 'Blog Style'),
        ('news', 'News Style'),
        ('external', 'External Style'),
    ]

    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="carousel/")
    alt_text = models.CharField(
        max_length=255,
        blank=True,
        help_text=(
            "Alternative text for accessibility"
        ),
    )
    style = models.CharField(
        max_length=10,
        choices=STYLE_CHOICES,
        default='external'
    )

    product = models.ForeignKey(
        'works.Product',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    blog_post = models.ForeignKey(
        'blog.Post',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    external_link = models.URLField(blank=True, null=True)
    open_in_new_tab = models.BooleanField(default=False)

    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(
        default=0,
        help_text="Order of appearance in carousel"
    )

    cta_text = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Call to Action button text"
    )
    cta_style = models.CharField(
        max_length=20,
        choices=[
            ('primary', 'Primary Button'),
            ('secondary', 'Secondary Button'),
            ('link', 'Link Style'),
        ],
        default='primary',
        blank=True,
        null=True
    )

    class Meta:
        """
        Meta class for CarouselItem model.
        """
        ordering = ['order', '-start_date']
        verbose_name = "Carousel Item"
        verbose_name_plural = "Carousel Items"

    def get_link(self):
        """
        Get the appropriate URL for the carousel item based on its style.
        """
        if self.style == 'product' and self.product:
            return self.product.get_absolute_url()
        elif self.style == 'blog' and self.blog_post:
            return self.blog_post.get_absolute_url()
        elif self.external_link:
            return self.external_link
        return "#"

    def is_visible(self):
        """
        Check if the carousel item should be visible based on dates and active status.
        """
        now = timezone.now()
        return (
            self.is_active and
            (self.start_date <= now) and
            (not self.end_date or self.end_date >= now)
        )

    def __str__(self):
        """
        String representation of the CarouselItem model.
        """
        return f"{self.title} ({self.style})"

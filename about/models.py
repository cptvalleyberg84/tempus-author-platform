from django.db import models
from django.core.validators import MinLengthValidator, EmailValidator


class CollaborationRequest(models.Model):
    """
    Model representing collaboration requests from users.

    This model stores and manages collaboration requests submitted through the
    about page form. It includes various types of collaboration requests such
    as project collaborations, mentorship, business opportunities, etc.
    """

    STATUS_CHOICES = [
        ('NEW', 'New'),
        ('READ', 'Read'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('DECLINED', 'Declined'),
    ]

    COLLABORATION_TYPES = [
        ('PROJECT', 'Project Collaboration'),
        ('MENTORSHIP', 'Mentorship'),
        ('BUSINESS', 'Business Opportunity'),
        ('INTERVIEW', 'Interview Request'),
        ('WRITING', 'Writing Partnership'),
        ('REVIEW', 'Book Review'),
        ('BETA', 'Beta Reading'),
        ('OTHER', 'Other'),
    ]

    name = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(6, "Name must be at least 6 characters long")
        ]
    )
    email = models.EmailField(
        validators=[EmailValidator()]
    )
    subject = models.CharField(
        max_length=200,
        help_text="Subject of the collaboration request (optional)",
        validators=[
            MinLengthValidator(
                6,
                "Subject must be at least 6 characters long"
                )],
        default="Hello There!"
        )
    collaboration_type = models.CharField(
        max_length=20,
        choices=COLLABORATION_TYPES,
        default='PROJECT'
    )
    message = models.TextField(
        validators=[
            MinLengthValidator(
                10, "Message must be at least 10 characters long"
            )
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='NEW'
    )
    is_read = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Meta class for CollaborationRequest model.

        Defines model-specific settings including ordering, indexes,
        and verbose names for admin interface.
        """
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['status']),
            models.Index(fields=['is_read']),
        ]
        verbose_name = 'Collaboration Request'
        verbose_name_plural = 'Collaboration Requests'

    def __str__(self):
        """
        Returns a string representation of the CollaborationRequest.
        """
        return (
            f"{self.name} - {self.collaboration_type} "
            f"({self.created_at.strftime('%Y-%m-%d')})"
        )

    def mark_as_read(self):
        """
        Marks the collaboration request as read.
        """
        if not self.is_read:
            self.is_read = True
            self.status = 'READ'
            self.save()

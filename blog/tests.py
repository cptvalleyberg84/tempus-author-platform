from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from .models import Post, Comment


class TestPostModel(TestCase):
    def setUp(self):
        # Create a test user (staff member)
        self.user = User.objects.create_user(
            username='teststaff',
            email='staff@example.com',
            password='testpass123',
            is_staff=True
        )
        
        # Create a test post
        self.post = Post.objects.create(
            post_title='Test Post',
            post_slug='test-post',
            post_author=self.user,
            post_content='This is a test post content.',
            post_status=1  # Published
        )

    def test_post_creation(self):
        """Test that a post can be created with correct initial values"""
        self.assertEqual(self.post.post_title, 'Test Post')
        self.assertEqual(self.post.post_slug, 'test-post')
        self.assertEqual(self.post.post_author, self.user)
        self.assertEqual(self.post.post_status, 1)
        self.assertTrue(self.post.post_created_on)
        self.assertTrue(self.post.post_updated_at)

    def test_post_str_representation(self):
        """Test the string representation of a Post"""
        self.assertEqual(str(self.post), 'Test Post')

    def test_post_excerpt_generation(self):
        """Test that post excerpt is automatically generated"""
        long_content = 'x' * 200  # Content longer than 150 characters
        post = Post.objects.create(
            post_title='Long Post',
            post_slug='long-post',
            post_author=self.user,
            post_content=long_content
        )
        self.assertEqual(len(post.post_excerpt), 153)  # 150 chars + '...'
        self.assertTrue(post.post_excerpt.endswith('...'))

    def test_empty_title_validation(self):
        """Test that empty or whitespace-only titles are not allowed"""
        with self.assertRaises(ValidationError):
            post = Post(
                post_title='   ',  # Only whitespace
                post_slug='empty-title',
                post_author=self.user,
                post_content='Content'
            )
            post.full_clean()


class TestCommentModel(TestCase):
    def setUp(self):
        # Create a test staff user (author)
        self.staff_user = User.objects.create_user(
            username='teststaff',
            email='staff@example.com',
            password='testpass123',
            is_staff=True
        )
        
        # Create a regular user (commenter)
        self.regular_user = User.objects.create_user(
            username='testuser',
            email='user@example.com',
            password='testpass123'
        )
        
        # Create a test post
        self.post = Post.objects.create(
            post_title='Test Post',
            post_slug='test-post',
            post_author=self.staff_user,
            post_content='This is a test post content.',
            post_status=1
        )
        
        # Create a test comment
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.regular_user,
            content='This is a test comment.'
        )

    def test_comment_creation(self):
        """Test that a comment can be created with correct values"""
        self.assertEqual(self.comment.post, self.post)
        self.assertEqual(self.comment.author, self.regular_user)
        self.assertEqual(self.comment.content, 'This is a test comment.')
        self.assertTrue(self.comment.active)
        self.assertTrue(self.comment.created_on)
        self.assertTrue(self.comment.updated_at)

    def test_comment_str_representation(self):
        """Test the string representation of a Comment"""
        expected = f'Comment by {self.regular_user} on {self.post}'
        self.assertEqual(str(self.comment), expected)

    def test_empty_comment_validation(self):
        """Test that empty or whitespace-only comments are not allowed"""
        with self.assertRaises(ValidationError):
            comment = Comment(
                post=self.post,
                author=self.regular_user,
                content='   '  # Only whitespace
            )
            comment.full_clean()

    def test_comment_ordering(self):
        """Test that comments are ordered by created_on date"""
        comment2 = Comment.objects.create(
            post=self.post,
            author=self.regular_user,
            content='Second comment'
        )
        comments = self.post.comments.all()
        self.assertEqual(comments[0], self.comment)  # First comment
        self.assertEqual(comments[1], comment2)  # Second comment

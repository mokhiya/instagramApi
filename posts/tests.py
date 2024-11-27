from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import PostModel

CustomUser = get_user_model()


class PostModelTestCase(TestCase):

    def setUp(self):
        """Set up test users and posts."""
        self.user1 = CustomUser.objects.create_user(username='user1', password='password123')
        self.user2 = CustomUser.objects.create_user(username='user2', password='password123')

        self.post1 = PostModel.objects.create(user=self.user1, text="This is the first post.")
        self.post2 = PostModel.objects.create(user=self.user2, text="This is the second post.", parent=self.post1)

    def test_post_creation(self):
        """Test that posts are created correctly."""
        self.assertEqual(self.post1.user, self.user1)
        self.assertEqual(self.post1.text, "This is the first post.")
        self.assertIsNone(self.post1.parent)
        self.assertIsNotNone(self.post1.created_at)

        self.assertEqual(self.post2.user, self.user2)
        self.assertEqual(self.post2.text, "This is the second post.")
        self.assertEqual(self.post2.parent, self.post1)

    def test_related_name_children(self):
        """Test the `children` related name for parent-child relationships."""
        children = self.post1.children.all()
        self.assertIn(self.post2, children)
        self.assertEqual(children.count(), 1)

    def test_related_name_posts(self):
        """Test the `posts` related name for user-post relationships."""
        posts_user1 = self.user1.posts.all()
        posts_user2 = self.user2.posts.all()

        self.assertIn(self.post1, posts_user1)
        self.assertEqual(posts_user1.count(), 1)

        self.assertIn(self.post2, posts_user2)
        self.assertEqual(posts_user2.count(), 1)

    def test_string_representation(self):
        """Test the string representation of the post model."""
        self.assertEqual(str(self.post1), "This is the first post.")
        self.assertEqual(str(self.post2), "This is the second post.")

    def test_ordering(self):
        """Test that posts are ordered by `created_at`."""
        post3 = PostModel.objects.create(user=self.user1, text="This is the third post.")
        posts = PostModel.objects.all()
        self.assertEqual(posts[0], self.post1)
        self.assertEqual(posts[1], self.post2)
        self.assertEqual(posts[2], post3)
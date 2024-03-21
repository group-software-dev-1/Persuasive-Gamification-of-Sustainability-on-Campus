from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from forum.models import Post, Suggestion, Annoucement, Comment

class TestSuggestionInstance(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        get_user_model().objects.create_user(email='test@email.com', password='testPassword')
        Suggestion.objects.create(poster=get_user_model().objects.get(pk=1),
                                  post_name='stest',
                                  post_text = 'stxt',
                                  post_date=timezone.now(),
                                  linked_announced=None,
                                  endorsements=5)
    def test_poster_label(self):
        instance = Suggestion.objects.get(id=1)
        field_label = instance._meta.get_field('poster').verbose_name
        self.assertEqual(field_label, 'Poster')
    
    def test_postname_label(self):
        instance = Suggestion.objects.get(id=1)
        field_label = instance._meta.get_field('post_name').verbose_name
        self.assertEqual(field_label, 'Post Name')
    
    def test_postxt_label(self):
        instance = Suggestion.objects.get(id=1)
        field_label = instance._meta.get_field('post_text').verbose_name
        self.assertEqual(field_label, 'Post Text')

    def test_postdate_label(self):
        instance = Suggestion.objects.get(id=1)
        field_label = instance._meta.get_field('post_date').verbose_name
        self.assertEqual(field_label, 'Date Posted')

    def test_endorsments_label(self):
        instance = Suggestion.objects.get(id=1)
        field_label = instance._meta.get_field('endorsements').verbose_name
        self.assertEqual(field_label, 'Endorsements')

    def test_linkedannounce_label(self):
        instance = Suggestion.objects.get(id=1)
        field_label = instance._meta.get_field('linked_announced').verbose_name
        self.assertEqual(field_label, 'Announcement')

    def test_user_id(self):
        instance = Suggestion.objects.get(pk=1)
        user = get_user_model().objects.get(pk=1)
        self.assertEqual(instance.poster.id, user.id)

    def test_link_default(self):
        instance = Suggestion.objects.get(pk=1)
        default = instance._meta.get_field('linked_announced').default
        self.assertEqual(default, None)

    def test_endorsement_default(self):
        instance = Suggestion.objects.get(pk=1)
        default = instance._meta.get_field('endorsements').default
        self.assertEqual(default, 0)

    def test_getPostText(self):
        instance = Suggestion.objects.get(pk=1)
        expected_text = 'stxt'
        self.assertEqual(expected_text, instance.get_post_text())

    def test_getPostText(self):
        instance = Suggestion.objects.get(pk=1)
        expected_text = 'stest'
        self.assertEqual(expected_text, instance.get_post_name())

        
class TestAnnouncementInstance(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        get_user_model().objects.create_user(email='test@email.com', password='testPassword')
        Annoucement.objects.create(poster=get_user_model().objects.get(pk=1),
                                  post_name='atest',
                                  post_text='atxt',
                                  post_date=timezone.now(),
                                  active=True)
        
    def test_poster_label(self):
        instance = Annoucement.objects.get(id=1)
        field_label = instance._meta.get_field('poster').verbose_name
        self.assertEqual(field_label, 'Poster')
    
    def test_postname_label(self):
        instance = Annoucement.objects.get(id=1)
        field_label = instance._meta.get_field('post_name').verbose_name
        self.assertEqual(field_label, 'Post Name')
    
    def test_postxt_label(self):
        instance = Annoucement.objects.get(id=1)
        field_label = instance._meta.get_field('post_text').verbose_name
        self.assertEqual(field_label, 'Post Text')

    def test_postdate_label(self):
        instance = Annoucement.objects.get(id=1)
        field_label = instance._meta.get_field('post_date').verbose_name
        self.assertEqual(field_label, 'Date Posted')

    def test_active_label(self):
        instance = Annoucement.objects.get(id=1)
        field_label = instance._meta.get_field('active').verbose_name
        self.assertEqual(field_label, 'Is Active')

    def test_user_id(self):
        instance = Annoucement.objects.get(pk=1)
        user = get_user_model().objects.get(pk=1)
        self.assertEqual(instance.poster.id, user.id)

    def test_active_default(self):
        instance = Annoucement.objects.get(pk=1)
        default = instance._meta.get_field('active').default
        self.assertEqual(default, True)

    def test_getPostText(self):
        instance = Annoucement.objects.get(pk=1)
        expected_text = 'atxt'
        self.assertEqual(expected_text, instance.get_post_text())

    def test_getPostText(self):
        instance = Annoucement.objects.get(pk=1)
        expected_text = 'atest'
        self.assertEqual(expected_text, instance.get_post_name())
        

class TestCommentInstance(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        get_user_model().objects.create_user(email='test@email.com', password='testPassword')
        Suggestion.objects.create(poster=get_user_model().objects.get(pk=1),
                                  post_name='stest',
                                  post_text = 'stxt',
                                  post_date=timezone.now(),
                                  linked_announced=None,
                                  endorsements=5)
        Comment.objects.create(poster=get_user_model().objects.get(pk=1),
                                  comment_text = 'ctxt',
                                  post_date=timezone.now(),
                                  linked_announcement=None,
                                  linked_post=Suggestion.objects.get(id=1),
                                  endorsements=5)
        
    def test_poster_label(self):
        instance = Comment.objects.get(id=1)
        field_label = instance._meta.get_field('poster').verbose_name
        self.assertEqual(field_label, 'Poster')
    
    def test_commmenttxt_label(self):
        instance = Comment.objects.get(id=1)
        field_label = instance._meta.get_field('comment_text').verbose_name
        self.assertEqual(field_label, 'Comment Text')

    def test_postdate_label(self):
        instance = Comment.objects.get(id=1)
        field_label = instance._meta.get_field('post_date').verbose_name
        self.assertEqual(field_label, 'Date Posted')

    def test_endorsments_label(self):
        instance = Comment.objects.get(id=1)
        field_label = instance._meta.get_field('endorsements').verbose_name
        self.assertEqual(field_label, 'Endorsements')

    def test_linkedpost_label(self):
        instance = Comment.objects.get(id=1)
        field_label = instance._meta.get_field('linked_post').verbose_name
        self.assertEqual(field_label, 'Suggestion')

    def test_linkedannounce_label(self):
        instance = Comment.objects.get(id=1)
        field_label = instance._meta.get_field('linked_announcement').verbose_name
        self.assertEqual(field_label, 'Announcement')

    def test_user_id(self):
        instance = Comment.objects.get(pk=1)
        user = get_user_model().objects.get(pk=1)
        self.assertEqual(instance.poster.id, user.id)

    def test_post_id(self):
        instance = Comment.objects.get(pk=1)
        originalpost = Suggestion.objects.get(pk=1)
        self.assertEqual(instance.poster.id, originalpost.id)

    def test_link_default(self):
        instance = Comment.objects.get(pk=1)
        default = instance._meta.get_field('linked_announcement').default
        self.assertEqual(default, None)

    def test_link_default(self):
        instance = Comment.objects.get(pk=1)
        default = instance._meta.get_field('linked_post').default
        self.assertEqual(default, None)

    def test_endorsement_default(self):
        instance = Comment.objects.get(pk=1)
        default = instance._meta.get_field('endorsements').default
        self.assertEqual(default, 0)


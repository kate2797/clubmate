from django.test import TestCase
from django.urls import reverse

from clubmate.models import Club


class ClubModelTests(TestCase):
    def setUp(self):
        club = \
            Club.objects.get_or_create(name='Test', club_description='Test', city='Test',
                                       website_url='https://swg3.tv/',
                                       genre='Test', location_coordinates='Test', opening_hours_week='Test',
                                       opening_hours_weekend='Test')[0]

    def test_ensure_min_entry_free_is_zero(self):
        """ Ensures that the default value for entry fee is zero. """
        club = Club.objects.get_or_create(name='Test')[0]
        self.assertEqual((club.entry_fee == 0.0), True)


class ClubDetailViewTests(TestCase):
    def test_club_detail_club_does_not_exist(self):
        """ If no categories exist, the appropriate message should be displayed. """
        response = self.client.get(reverse('clubmate:club_detail', kwargs={'club_id': 1000}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'The specified club does not exist')
        self.assertIsNone(response.context['club'])


class DiscoverViewTests(TestCase):
    def setUp(self):
        inn_deep = \
            Club.objects.get_or_create(name='Inn Deep', club_description='Test', city='Test',
                                       website_url='https://swg3.tv/',
                                       genre='Test', location_coordinates='Test', opening_hours_week='Test',
                                       opening_hours_weekend='Test')[0]

        swg3 = \
            Club.objects.get_or_create(name='SWG3', club_description='Test', city='Test',
                                       website_url='https://swg3.tv/',
                                       genre='Test', location_coordinates='Test', opening_hours_week='Test',
                                       opening_hours_weekend='Test')[0]

    def test_clubs_display_correctly_on_discover(self):
        """ Checks if clubs are correctly retrieved from the database on Discover. """
        count = Club.objects.count()
        self.assertEqual(count, 2)


class IndexViewTests(TestCase):
    def test_index_subheading(self):
        """ Checks if the HTML subheading of the homepage is correctly displayed. """
        response = self.client.get(reverse('clubmate:index'))
        subheading = '<h4 class="mt-3 mb-3">Student clubbing made fun, safe and easy 🥤</h4>' in response.content.decode()
        self.assertTrue(subheading)

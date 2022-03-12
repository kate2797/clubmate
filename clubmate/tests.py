from django.test import TestCase
from django.urls import reverse

from clubmate.models import Club


def create_dummy_club(name):
    club = Club.objects.get_or_create(name=name, club_description='test', city='test', website_url='https://swg3.tv/',
                                      genre='test', location_coordinates='test', opening_hours_week='test',
                                      opening_hours_weekend='test', picture='event_pictures/default_event.png')[0]
    return club


class ClubModelTests(TestCase):
    """ Ensures that the default value for entry fee is zero. """
    def test_ensure_min_entry_free_is_zero(self):
        club = create_dummy_club('SWG3')
        self.assertEqual((club.entry_fee == 0.0), True)


class ClubDetailViewTests(TestCase):
    def test_club_detail_club_does_not_exist(self):
        """ If no categories exist, the appropriate message should be displayed. """
        response = self.client.get(reverse('clubmate:club_detail', kwargs={'club_id': 1000}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'The specified club does not exist')
        self.assertIsNone(response.context['club'])


class DiscoverViewTests(TestCase):
    pass

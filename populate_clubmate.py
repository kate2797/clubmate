import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clubmate_project.settings')

import django

django.setup()
from clubmate.models import Club, Event, Rating, UserProfile
from django.contrib.auth.models import User

import dateutil.parser


def populate():
    users = {
        'averagestudent': {'password': 'averagestudent',
                           'email': 'averagestudent@averagestudent.com',
                           'first_name': 'Sarah-Jayne',
                           'last_name': 'Barr',
                           'bio': 'One day, I hope to be a happily married old man telling wild stories from his wild youth',
                           'is_club_owner': 'False'},

        'ironmansnap': {
            'password': 'ironmansnap',
            'email': 'ironmansnap@ironmansnap.com',
            'first_name': 'Anwen',
            'last_name': 'Metcalfe',
            'bio': 'Currently hanging out in 🇵🇹',
            'is_club_owner': 'False'},

        'ghostfacegangsta': {'password': 'ghostfacegangsta',
                             'email': 'ghostfacegangsta@ghostfacegangsta.com',
                             'first_name': 'Charis',
                             'last_name': 'Singh',
                             'bio': 'People call me Michael but you can call me tonight 😉',
                             'is_club_owner': 'False'},

        'MrsDracoMalfoy': {'password': 'MrsDracoMalfoy',
                           'email': 'MrsDracoMalfoy@MrsDracoMalfoy.com',
                           'first_name': 'Agnès',
                           'last_name': 'Wright',
                           'bio': 'Gamer. Alcohol fanatic. Coffee practitioner.',
                           'is_club_owner': 'False'},

        'emilyramo': {
            'password': 'emilyramo',
            'first_name': 'Emily',
            'last_name': 'Ramo',
            'email': 'emilyramo@emilyramo.com',
            'bio': '😉',
            'is_club_owner': 'False'},

        'RidleyRich': {
            'password': 'RidleyRich',
            'email': 'RidleyRich@RidleyRich.com',
            'first_name': 'Ridley',
            'last_name': 'Preston',
            'bio': 'Thank you, come again',
            'is_club_owner': 'True'},

        'SuperMagnificentExtreme': {
            'password': 'SuperMagnificentExtreme',
            'first_name': 'Konrad',
            'last_name': 'Chen',
            'email': 'SuperMagnificentExtreme@SuperMagnificentExtreme.com',
            'bio': 'Thank you, come again',
            'is_club_owner': 'True'},
    }

    user_map = {}
    for username, data in users.items():
        u = add_user(username, data['password'], data['email'], data['bio'], data['first_name'],
                     data['last_name'], data['is_club_owner'])
        user_map[username] = u
        print(f'– {u} was added')

    clubs = {
        'SWG3': {
            'club_description': 'SWG3 is an arts and events venue in Glasgow, offering everything from pulsing club nights, to cutting-edge art, to creative workspaces and studios.',
            'city': 'Glasgow',
            'website_url': 'https://swg3.tv/',
            'genre': 'Techno',
            'location_coordinates': '55.86479 -4.29999',
            'entry_fee': '8.0',
            'opening_hours_week': '12PM–12AM',
            'opening_hours_weekend': '12PM–12AM',
            'picture': 'club_pictures/swg3.jpeg',
            'covid_test_required': 'True',  # Change to human-friendly names next time
            'underage_visitors_allowed': 'True',
            'average_rating': '0.0',
            'user_reported_safety': 'False'
        },

        'Inn Deep': {
            'club_description': 'Craft ale pub with an arched wooden ceiling, a terrace, quirky murals and an American-style menu.',
            'city': 'Glasgow',
            'website_url': 'https://www.inndeep.com/',
            'genre': 'Alternative',
            'location_coordinates': '55.87473 -4.27969',
            'entry_fee': '5.0',
            'opening_hours_week': '10AM–6PM',
            'opening_hours_weekend': '10AM–4AM',
            'picture': 'club_pictures/inndeep.jpeg',
            'covid_test_required': 'False',
            'underage_visitors_allowed': 'True',
            'average_rating': '0.0',
            'user_reported_safety': 'False'
        },

        'Sub Club': {
            'club_description': 'The Sub Club is a club and music venue located at 22 Jamaica Street in Glasgow, Scotland. It opened 1 April 1987 and is the longest running underground dance club in the world.',
            'city': 'Glasgow',
            'website_url': 'https://subclub.co.uk/',
            'genre': 'House',
            'location_coordinates': '55.858 -4.2574',
            'entry_fee': '9.0',
            'opening_hours_week': '6PM–3AM',
            'opening_hours_weekend': '6PM–6AM',
            'picture': 'club_pictures/subclub.png',
            'covid_test_required': 'False',
            'underage_visitors_allowed': 'False',
            'average_rating': '0.0',
            'user_reported_safety': 'False'},
    }

    club_map = {}
    for name, data in clubs.items():
        c = add_club(name, data['club_description'], data['city'], data['website_url'], data['genre'],
                     data['location_coordinates'],
                     data['entry_fee'], data['opening_hours_week'], data['opening_hours_weekend'], data['picture'],
                     data['covid_test_required'], data['underage_visitors_allowed'])
        club_map[name] = c
        print(f'– {c} was added')

    events = {
        'The Blinders': {
            'club': club_map['SWG3'],
            'picture': 'event_pictures/swg3_theblinders.jpg',
            'happening_at': dateutil.parser.parse('04/14/22 23:00'),
            'capacity': '200'
        },

        'Pool Party': {
            'club': club_map['SWG3'],
            'picture': 'event_pictures/swg3_poolparty.jpg',
            'happening_at': dateutil.parser.parse('05/11/22 23:00'),
            'capacity': '200'
        },

        'Palaye Royale': {
            'club': club_map['Inn Deep'],
            'picture': 'event_pictures/inndeep_palayeroyale.jpg',
            'happening_at': dateutil.parser.parse('03/31/22 20:00'),
            'capacity': '100'
        },

        'Subculture with Harri & Domenic': {
            'club': club_map['Sub Club'],
            'picture': 'event_pictures/subclub_subculture.jpg',
            'happening_at': dateutil.parser.parse('03/29/22 22:00'),
            'capacity': '150'
        },

        'ALL U NEED XL': {
            'club': club_map['Sub Club'],
            'picture': 'event_pictures/subclub_alluneedxl.jpg',
            'happening_at': dateutil.parser.parse('06/06/22 20:00'),
            'capacity': '150'
        },
    }

    for title, data in events.items():
        e = add_event(title, data['club'], data['picture'], data['happening_at'], data['capacity'])
        print(f'– {e} was added')

    ratings = [
        {'title': 'Great club',
         'club': club_map['SWG3'],
         'author': user_map['averagestudent'],
         'rating_score': '4.5',
         'is_safe': 'True',
         'user_commentary': "Awesome vibes, great club. A true gem. Their door policy is the best. 'Why are you here?' Perfect question. I always tell my friends about this place and the bouncer and the rumour about how the only fight ever to break out in the place was met by the dancers being so offended they took it upon themselves to throw the perpetrators themselves out the doors and into traffic. Staff hadn't needed to a thing. Who knows if it's true. Legend.",
         'posted_at': dateutil.parser.parse('01/31/22 23:22'),
         'number_of_upvotes': '23',
         },

        {'title': 'Good but would not recommend',
         'club': club_map['SWG3'],
         'author': user_map['ironmansnap'],
         'rating_score': '2.0',
         'is_safe': 'False',
         'user_commentary': "It's a good place, but it's very dangerous outside. Yesterday was my first day in Glasgow, and we've been attacked by 5 people. 1 girl 4 boys. So we had to leave the place...",
         'posted_at': dateutil.parser.parse('01/21/22 13:05'),
         'number_of_upvotes': '67',
         },

        {'title': 'Do not go there',
         'club': club_map['Inn Deep'],
         'author': user_map['ghostfacegangsta'],
         'rating_score': '1.0',
         'is_safe': 'False',
         'user_commentary': "Unbelievably disappointed. Entry was over 11 quid and pre booked ticket only, go buy two drinks, dance with my girlfriend for less than an hour. A bouncer comes into the the dance floor and tells me I have to leave and takes me outside, completely unwarranted. Girlfriend also had to leave after paying 11 quid. Would not recommend.",
         'posted_at': dateutil.parser.parse('01/01/22 17:55'),
         'number_of_upvotes': '107',
         },

        {'title': 'Do not support this club',
         'club': club_map['Sub Club'],
         'author': user_map['MrsDracoMalfoy'],
         'rating_score': '1.0',
         'is_safe': 'False',
         'user_commentary': "Please do not support this club. I came up to Glasgow as an early birthday treat to see my friend. When we were in the queue and tried to enter the club, an extremely arrogant and rude bouncer randomly selected myself and my friend and told us we were not allowed in for being ‘too drunk’.",
         'posted_at': dateutil.parser.parse('12/03/22 10:55'),
         'number_of_upvotes': '38',
         },

        {'title': 'Great nights, little mad but love it',
         'club': club_map['Sub Club'],
         'author': user_map['ghostfacegangsta'],
         'rating_score': '3.5',
         'is_safe': 'True',
         'user_commentary': "Make sure you know who is playing or you won’t get in. Great nights, little mad but love it. Speaker system is unreal.",
         'posted_at': dateutil.parser.parse('01/03/22 17:00'),
         'number_of_upvotes': '7',
         },
    ]

    for rating in ratings:
        r = add_rating(rating['title'], rating['club'], rating['author'], rating['rating_score'], rating['is_safe'],
                       rating['user_commentary'], rating['posted_at'], rating['number_of_upvotes'])
        print(f'– {r} was added')

    # Add some clubs as "saved clubs" to some users, to make it look more natural instead of adding all to all
    user_map['MrsDracoMalfoy'].clubs.add(club_map['SWG3'])
    user_map['ghostfacegangsta'].clubs.add(club_map['SWG3'])
    user_map['ghostfacegangsta'].clubs.add(club_map['Sub Club'])
    user_map['averagestudent'].clubs.add(club_map['SWG3'])
    user_map['averagestudent'].clubs.add(club_map['Inn Deep'])
    user_map['emilyramo'].clubs.add(club_map['Inn Deep'])


def add_user(username, password, email, bio, first_name, last_name, is_club_owner):
    u = User(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
    u.save()
    cu = UserProfile.objects.get_or_create(user=u)[0]  # cu – clubmate user
    cu.bio = bio  # Set the bio
    cu.is_club_owner = is_club_owner
    cu.save()
    return cu


def add_club(name, club_description, city, website_url, genre, location_coordinates, entry_fee, opening_hours_week,
             opening_hours_weekend, picture, covid_test_required, underage_visitors_allowed):
    c = Club.objects.get_or_create(name=name, club_description=club_description, city=city, website_url=website_url,
                                   genre=genre, location_coordinates=location_coordinates, entry_fee=entry_fee,
                                   opening_hours_week=opening_hours_week,
                                   opening_hours_weekend=opening_hours_weekend, picture=picture,
                                   covid_test_required=covid_test_required,
                                   underage_visitors_allowed=underage_visitors_allowed)[0]
    c.average_rating = 0.0  # Default
    c.user_reported_safety = False  # Default
    c.save()
    return c


def add_rating(title, club, author, rating_score, is_safe, user_commentary, posted_at, number_of_upvotes):
    r = Rating.objects.get_or_create(title=title, club=club, author=author, rating_score=rating_score,
                                     is_safe=is_safe, user_commentary=user_commentary, posted_at=posted_at,
                                     number_of_upvotes=number_of_upvotes)[0]
    r.user_reported_safety = False  # Default
    r.save()
    return r


def add_event(title, club, picture, happening_at, capacity):
    e = Event.objects.get_or_create(title=title, club=club, picture=picture, happening_at=happening_at,
                                    capacity=capacity)[0]
    e.save()
    return e


if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()

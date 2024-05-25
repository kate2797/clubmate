# ClubMate

Venturing into the club scene during your university days can be thrilling yet daunting. Enter ClubMate: your go-to companion for navigating the UK's nightlife safely and sensibly. Catering to both eager freshers and seasoned students, ClubMate offers a platform where users can rate and review venues, ensuring a vibrant yet secure clubbing experience.

But ClubMate isn't just for the partygoers; it's a lifeline for club owners too. Amidst the pandemic's challenges, ClubMate provides a spotlight for venues, allowing owners to showcase their offerings and safety measures, attracting students eager for a night out.

Designed by Group 33 as part of the ITECH 21-22 module, ClubMate is more than just an app; it's a community-driven initiative prioritising student well-being. Dive into the world of ClubMate and discover a new era of club rating applications.

Curious to see the project's visual journey? Check out our wireframes on AdobeXD [here](https://xd.adobe.com/view/48d98a5e-9a3f-4c8a-84ab-2eb515e9cdd6-1d8a/).

## Getting Started
To set up the project on your machine, kindly follow the instructions below for cloning and installation.

### Cloning
```
git clone https://github.com/kate2797/clubmate_project
cd clubmate_project
```
### Virtual Environment
Activate the project's virtual environment using Anaconda.

```
$ conda create -n clubmate python=3.7.5
$ conda activate clubmate
```
### Dependencies
For the project to run properly, all packages from the `requirements.txt` file need to be installed prior. To install them, please run the command below.
```
(clubmate) $ pip install -r requirements.txt
```

### Installation
Before starting the application server, please run the following commands to configure and pre-populate the database with useful data.
```
(clubmate) $ python manage.py makemigrations clubmate
(clubmate) $ python manage.py migrate
(clubmate) $ python populate_clubmate.py
```
Finally, start the application server and navigate to port [127.0.0.1:8000](http://127.0.0.1:8000/) to view the project.
```
(clubmate) $ python manage.py runserver
```
### Usage
Although the web application allows new students and club owners to register and login, it also comes pre-populated with several student and club owner users. Please see the credentials below to login as one of the existing users and note that, in all cases, the password is the same as username. However, many parts of the application are also accessible to users without a ClubMate account, such as the Discover or Ratings page.

#### Student Credentials
- averagestudent
- ironmansnap
- ghostfacegangsta
- MrsDracoMalfoy
- emilyramo

#### Club Owner Credentials
- RidleyRich
- SuperMagnificentExtreme

### Testing
The project comes with several unit tests testing its implementation. To run the tests yourself, please run the following command after stopping the application server.
```
(clubmate) $ python manage.py test
```
## Technologies
Several technologies were used to build this project. Please see the full list below.
- Python 3.7
- Django 2.1
- SQLite3
- Bootstrap 5
- HTML5
- CSS3
- JavaScript ES6

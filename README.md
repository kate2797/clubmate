# ClubMate
Going clubbing during your university years can be very enjoyable but also risky. How does one know if the new club in the town is good? Club ratings to the rescue. The aim of ClubMate is to help guide rave-seeking freshers and the student population more broadly through a plethora of venues and clubs throughout the UK not only to get their money's worth, but also ensure they are clubbing safely. Students will have to create an account to be able to leave ratings for clubs and vote for existing ratings.

ClubMate also intends to help club owners get their clubs noticed amid the losses from the pandemic. Club owners can list their venues on ClubMate and include venue address, opening times, a small description of the bar and where it is on a map, so that students can easily choose the venue of their choice for the night.

Students can browse and select clubs depending on their location, genre, and criteria such as whether 18+ entry or COVID test are required, user reviews of the venues in terms of the club’s number of stars, user commentary, and whether a club is deemed safe by others. Through its focus on student health safety, ClubMate brings a new spin-off to traditional club rating applications.

The project was developed by Group 33 as an assessed coursework for the ITECH 21-22 module and is hosted on PythonAnywhere under the following link: TODO. To see the wireframes that guided the visuals of the project, visit this [AdobeXD](https://xd.adobe.com/view/48d98a5e-9a3f-4c8a-84ab-2eb515e9cdd6-1d8a/) link.

## Getting Started
To run the project on your machine, please follow the instructions below to clone and install the project properly.

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
To properly run the project, several packages from the `requirements.txt` file need to be installed prior. To install them, run the command below.
```
(clubmate) $ pip install -r requirements.txt
```
To install system-level dependencies, please also run the following, to install the dateutil and six package.
```
(clubmate) $ pip install python-dateutil
(clubmate) $ pip install six
```
### Installation
Before starting the application server, please run the following commands to configure and pre-populate the database with useful data.
```
(clubmate) $ python manage.py makemigrations
(clubmate) $ python manage.py migrate
(clubmate) $ python populate_clubmate.py
```
Finally, start the application server and go to port [127.0.0.1:8000](http://127.0.0.1:8000/) to view the project.
```
(clubmate) $ python manage.py runserver
```
### Usage
Although the web application allows new students and club owners to register and login, it also comes pre-populated with several student and club owner users. Please see the credentials below to login as one of the existing users and note that, in all cases, the password is the same as username.
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
Several technologies, packages and libraries were used to build this project. Please see the full list below.
- TODO
- TODO
- TODO
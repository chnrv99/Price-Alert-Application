# Backend Task - Price Application

## Description
To create a application which triggers an alert when a specific range of price is achieved for a cryptocurrency

## REST APIs
### Authentication 
 /accounts/login -> used django-allauth + google OAuth to login  
 /accounts/logout -> for logging out  

### Alerts (all are protected)
 /alerts/fetch GET -> to fetch the records. Used redis for caching 2mins timeout. Has 2 url params: type and page, type represents created/triggered alerts, page represents the pagination(each page has 3 records for now)  
 /alerts/create POST -> to create an alert, takes in 3 parameters: coin, target_price, flag_trigger, user  
 /alerts/delete DELETE -> deletes an alert based on alert_idg  

## Database relation
Used ER to Relation mapping, and some tweaks to reduce the number of tables from 5 to  4. The tables mentioned in the diagram are in 3NF.  

## Caching and mailing
Used redis to cache /alerts/fetch  
Used redis + celery as a queuing for email, using SMTP Gmail for mailing  

## Run the app using Docker
Used docker to bundle and contanerise the app.  
```
git clone https://github.com/chnrv99/Price-Alert-Application.git .
docker-compose build
docker-compose up
```
Application will be accessible in port 8000

## Demo Video
https://drive.google.com/file/d/1b8rHByDGUpKsBF7ptZqQq0YzFHHYb7-5/view?usp=sharing  

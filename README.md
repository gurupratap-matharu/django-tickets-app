# Ticket Register

A django projects that registers tickets for support based on 

* Category
* Severity
* Creation Date
* Expiry Date (calculating this is the most trickiest part of the app)
* Vendor
* Status

## Types of tickets

Tickets can be configure in the admin area but are generally divided into these common types.

* severity 1 to be resolved in 4 hours
* severity 2 to be resolved in 24 hours
* severity 3 to be resolved in 72 hours / 3 days
* severity 4 to be resolved in 168 hours / 7 days
* severity 5 to be resolved in 720 hours / 30 days

The interface itself permits

* To register a new ticket
* To see a list of all the tickets

## License

This code is open source. So feel free to use, modify, share, download as per your need. I do not take risk nor responsibility for your errors or any commercial damage.

## How to run?

This code is written in python3.7

## On local machine

Go to the mysite project folder that contains the manage.py file and then
```
python manage.py runserver
```

Else directly access the webapp on this link

http://gurupratap.pythonanywhere.com/support/

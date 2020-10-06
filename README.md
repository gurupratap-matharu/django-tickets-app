# Ticket Register

A web application that registers tickets for support based on

* Category
* Severity
* Creation Date
* Expiry Date
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

MIT License

## How to run

Go to the mysite project folder that contains the manage.py file and then

```
python manage.py runserver
```

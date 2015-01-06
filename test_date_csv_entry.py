import csv
import datetime

from django.contrib.auth.models import User
from django.db import models

from testive.events.models import TestDate, UserTestDate
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime

csv_file = open('testsheet.csv', 'rb')

#Read in the csv file
entries = csv.reader(csv_file)
entries.next() #skip the first line

#Get list of current UserTestDate from database
lookup = UserTestDate.objects.all()
alldates = TestDate.objects.all()
allusers = User.objects.all() #get database list of all users


#Loop through each line of csv
for row in entries:
	try: #check if date is correct format
		datetime.strptime(row[1], '%Y-%m-%d')
		theuser = allusers.get(email=row[0]) #get the user with matching email
		thedate = alldates.get(date=row[1])
		try: #is the given email found in the current list of usertestdates
			next = lookup.get(user__email=row[0]) #look for a database entry with the given csv email
			if next.test_date.date != thedate.date:
				next.update(test_date=thedate) #update the date if not equal
		except ObjectDoesNotExist: #email not found
			try: #determine if email is a registered user in database
				lookup.create(theuser, thedate) #create new entry in the usertestdata table
			except ObjectDoesNotExist: #email is not a registered user
				print 'Given email is not a registered user'
	except ValueError:
		print 'Given date is not in YYYY-MM-DD format'






from linkedin import linkedin
import json
from prettytable import PrettyTable

CONSUMER_KEY = ''									                          # API key
CONSUMER_SECRET = ''							                          # API secret

USER_SECRET = ''   			                                    # OAuth Secret
USER_TOKEN = ''                                             # OAuth Token
RETURN_URL = ''													                    # Empty for developer authentication

auth = linkedin.LinkedInDeveloperAuthentication(CONSUMER_KEY, CONSUMER_SECRET, 
          USER_TOKEN, USER_SECRET, 
          RETURN_URL, 
          permissions=linkedin.PERMISSIONS.enums.values())


app = linkedin.LinkedInApplication(auth)						# Passing keys tokens and permissions to app
profile = app.get_profile()									        # getting profile details

# getting user's info

print '-'*50
print profile['firstName'] + ' ' + profile['lastName'] 
print profile['siteStandardProfileRequest']['url']
full_profile = app.get_profile(selectors=['id', 'first-name', 'last-name', 'location', 'distance', 'num-connections', 'skills', 'educations', 'email-address', 'positions'])
print full_profile['emailAddress']
print full_profile['positions']	
print '-'*50

#print full_profile['skills']['values']
connections = app.get_connections()
count = connections['_total']

pt = PrettyTable(field_names=['Name', 'Location', 'Profile Link'])
pt.align = 'l'

[ pt.add_row((c['firstName'] + ' ' + c['lastName'], c['location']['name'], c['siteStandardProfileRequest']['url'])) 
  for c in connections['values']
      if c.has_key('location')]

print pt

# Prints connection names, start date, position name

try:
  for i in range(count):
    print '='*20
    print connections['values'][i]['firstName'] + ' ' + connections['values'][i]['lastName']
    print '='*20
    connection_id = connections['values'][i]['id']
    connection_positions = app.get_profile(member_id=connection_id, 
                                       selectors=['positions'])
    #print app.get_profile(connection_id, '')
    #print json.dumps(connection_positions, indent=1)
    if connection_positions['positions'].has_key('values'):
      for elem in connection_positions['positions']['values']:
        print '-'*20
        print 'Started Since : ',
        if elem['startDate'].has_key('month'):
          print str(elem['startDate']['month']) + ' /',  
        if elem['startDate'].has_key('year'):
          print str(elem['startDate']['year'])  
        print elem['title']
        print elem['company']['name']
        #print elem['startDate']['month'] + ' ' + elem['startDate']['year']

        #print json.dumps(connection_positions, indent=1)
except Exception, e:
  print e


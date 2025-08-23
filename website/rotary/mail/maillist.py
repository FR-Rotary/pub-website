from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from flask import current_app
import re

SCOPES = ['https://www.googleapis.com/auth/admin.directory.group', 'https://www.googleapis.com/auth/admin.directory.group.member', 'https://apps-apis.google.com/a/feeds/groups/']
SERVICE_ACCOUNT_FILE = '/app/rotary/secretKey.json'
credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES, subject='sudo@rotarypub.se')


def getMembersFromGroup(service, groupEmail):
    members = []
    try: 
        request = service.members().list(groupKey=groupEmail, maxResults=200)
        response = request.execute()
    except HttpError as e:
        current_app.logger.warning('Error response status code : {0}, reason : {1}'.format(e.status_code, e.error_details))
    if "members" in response:
        members = list(map(lambda x: x["email"], response["members"]))
    morePages = "nextPageToken" in response
    while morePages:
        try: 
            request = service.members().list_next(request, response)
            response = request.execute()
        except HttpError as e:
            current_app.logger.warning('Error response status code : {0}, reason : {1}'.format(e.status_code, e.error_details))
        if "members" in response:
            members = members + list(map(lambda x: x["email"], response["members"]))
        morePages = "nextPageToken" in response
    return members

def addMembersToGroup(service, groupEmail, emails):
    if len(emails) == 0:
        return
    current_app.logger.info("Adding {0} to {1}".format(emails, groupEmail))
    emails = list(map(lambda email: {
          "email": email,
          "kind": "member"
        }, emails))
    for email in emails:
        try: 
            response = service.members().insert(groupKey=groupEmail, body=email).execute()
        except HttpError as e:
            current_app.logger.warning('Error response status code : {0}, reason : {1}'.format(e.status_code, e.error_details))

def removeMembersFromGroup(service, groupEmail, emails):
    if len(emails) == 0:
        return
    current_app.logger.info("Deleting {0} from {1}".format(emails, groupEmail))
    for email in emails:
        try: 
            response = service.members().delete(groupKey=groupEmail, memberKey=email).execute()
        except HttpError as e:
            current_app.logger.warning('Error response status code : {0}, reason : {1}'.format(e.status_code, e.error_details))

def getUniquesInBothLists(emails1, emails2):
    emails1 = list(map(lambda x: x.lower(), emails1))
    emails2 = list(map(lambda x: x.lower(), emails2))
    emails1.sort()
    emails2.sort()
    uniqueEmails1 = []
    uniqueEmails2 = []
    while len(emails1) > 0 and len(emails2) > 0:
        if emails1[0] > emails2[0]:
            email = emails2.pop(0)
            uniqueEmails2.append(email)
        elif emails1[0] == emails2[0]:
            emails1.pop(0)
            emails2.pop(0)
        else:
            email = emails1.pop(0)
            uniqueEmails1.append(email)
    uniqueEmails1 = uniqueEmails1 + emails1
    uniqueEmails2 = uniqueEmails2 + emails2
    return (uniqueEmails1, uniqueEmails2)

def remove_from_maillists(groupKeys, memberToRemove):
    current_app.logger.info("Removing {0} from the following maillists: {1}".format(memberToRemove, groupKeys))
    service = build('admin', 'directory_v1', credentials=credentials)
    for groupKey in groupKeys:
        removeMembersFromGroup(service, groupKey, [memberToRemove])
    service.close()

def add_to_maillists(groupKeys, memberToAdd):
    current_app.logger.info("Adding {0} to the following maillists: {1}".format(memberToAdd, groupKeys))
    service = build('admin', 'directory_v1', credentials=credentials)
    for groupKey in groupKeys:
        addMembersToGroup(service, groupKey, [memberToAdd])
    service.close()

def update_maillist(groupKey, desiredMembers, removeMissing):
    service = build('admin', 'directory_v1', credentials=credentials)
    actualTestGroupMembers = getMembersFromGroup(service, groupKey)
    desiredTestGroupMembers = desiredMembers
    current_app.logger.info("Updating maillist for {0} with {1} desired members and {2} actual members".format(groupKey, len(desiredMembers), len(actualTestGroupMembers)))

    toRemove, toAdd = getUniquesInBothLists(actualTestGroupMembers, desiredTestGroupMembers)
    addMembersToGroup(service, groupKey, toAdd)
    if removeMissing:
        removeMembersFromGroup(service, groupKey, toRemove)
    service.close()

def is_valid_email(email):
    return re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)


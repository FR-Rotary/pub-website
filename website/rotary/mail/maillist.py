from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/admin.directory.group', 'https://www.googleapis.com/auth/admin.directory.group.member', 'https://apps-apis.google.com/a/feeds/groups/']
SERVICE_ACCOUNT_FILE = '/app/rotary/secretKey.json'
credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES, subject='sudo@rotarypub.se')


def getMembersFromGroup(groupEmail):
    service = build('admin', 'directory_v1', credentials=credentials)
    
    
    try: 
        response = service.members().list(groupKey=groupEmail).execute()
    except HttpError as e:
        print('Error response status code : {0}, reason : {1}'.format(e.status_code, e.error_details))
    
    service.close()
    
    members = []
    if "members" in response:
        members = response["members"]
        members = list(map(lambda x: x["email"], members))
    return members

def addMembersToGroup(groupEmail, emails):
    if len(emails) == 0:
        return
    print("Adding {0} emails from {1}".format(len(emails), groupEmail))
    emails = list(map(lambda email: {
          "email": email,
          "kind": "member"
        }, emails))
    service = build('admin', 'directory_v1', credentials=credentials)
    for email in emails:
        try: 
            response = service.members().insert(groupKey=groupEmail, body=email).execute()
        except HttpError as e:
            print('Error response status code : {0}, reason : {1}'.format(e.status_code, e.error_details))
    service.close()

def removeMembersToGroup(groupEmail, emails):
    if len(emails) == 0:
        return
    print("Deleting {0} emails from {1}".format(len(emails), groupEmail))
    service = build('admin', 'directory_v1', credentials=credentials)
    for email in emails:
        try: 
            response = service.members().delete(groupKey=groupEmail, memberKey=email).execute()
        except HttpError as e:
            print('Error response status code : {0}, reason : {1}'.format(e.status_code, e.error_details))
    service.close()

def getUniquesInBothLists(emails1, emails2):
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


def updateGroupToDesired(groupKey, desiredMembers):
    actualTestGroupMembers = getMembersFromGroup("test@rotarypub.se")
    desiredTestGroupMembers = desiredMembers

    toRemove, toAdd = getUniquesInBothLists(actualTestGroupMembers, desiredTestGroupMembers)
    print(toRemove, toAdd)
    addMembersToGroup("test@rotarypub.se", toAdd)
    removeMembersToGroup("test@rotarypub.se", toRemove)

def update_maillist(groupKey, desiredMembers):
    ##updateGroupToDesired("test@rotarypub.se", ["kryddan@rotarypub.se", "kaffe@rotarypub.se", "erik@ortenberg.se", "another@gmail.com"])
    return getMembersFromGroup(groupKey)

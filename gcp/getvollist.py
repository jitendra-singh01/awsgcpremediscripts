from pprint import pprint

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
credentials = GoogleCredentials.get_application_default()

service = discovery.build('compute', 'v1', credentials=credentials)

# Project ID for this request.
project = 'central-diode-250514'  # TODO: Update placeholder value.

def getZoneVollist(zone):
    print(zone)
    request = service.disks().list(project=project, zone=zone,filter="(status=READY) AND (lastDetachTimestamp!=\"\" OR lastAttachTimestamp=\"\")")
    while request is not None:
        response = request.execute()
        if 'items' in response and 'status' in response['items'][0]:
            for disk in response['items']:
                # TODO: Change code below to process each `disk` resource:
                print("not Attached Disk volume: {}, Size: {} GB at zone {}".format(disk['name'], disk['sizeGb'],zone))

            request = service.disks().list_next(previous_request=request, previous_response=response)
        else:
            print("not disk found: {} zone".format(zone))
            break

if __name__== "__main__":       
    request = service.zones().list(project=project)
    while request is not None:
        response = request.execute()
        for zone in response['items']:
            # TODO: Change code below to process each `zone` resource:
            tzone = zone['name']
            getZoneVollist(tzone)
        request = service.zones().list_next(previous_request=request, previous_response=response)

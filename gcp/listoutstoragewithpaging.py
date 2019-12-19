from google.cloud import storage

# Instantiates a client
storage_client = storage.Client()
nextPageToken = None
get_files=[]
def listoutbuckets(nextPageToken):
    if nextPageToken is None:
        iterator=storage_client.list_buckets(max_results=2,fields='items(name),nextPageToken')      
    else:
        iterator=storage_client.list_buckets(max_results=2,fields='items(name),nextPageToken',page_token=nextPageToken)
    pages = iterator.pages        
    for page in pages:
        for bucket in list(page):
            iam_configuration = bucket.iam_configuration
            policies = bucket.get_iam_policy()
            for role in policies:
                members = policies[role]
                member = list(members)[0]
                if role == "roles/storage.objectViewer" and member == "allUsers":
                    print("{} bucket is public".format(bucket.name))
                    #get_files.append("gs://" + f.name + "/" + f.name)

    if iterator.next_page_token is not None:
        listoutbuckets(iterator.next_page_token)
listoutbuckets(nextPageToken)
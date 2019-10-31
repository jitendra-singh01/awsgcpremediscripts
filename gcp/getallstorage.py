from google.cloud import storage

# Instantiates a client
storage_client = storage.Client()
for bucket in storage_client.list_buckets():
    iam_configuration = bucket.iam_configuration
    policies = bucket.get_iam_policy()
    print(bucket.metageneration)
    for role in policies:
        members = policies[role]
        member = list(members)[0]
        if role == "roles/storage.objectViewer" and member == "allUsers":
            print("{} bucket is public".format(bucket.name))

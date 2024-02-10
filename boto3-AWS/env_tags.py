import boto3

ec2_client_US_E = boto3.client('ec2', region_name='us-east-1')
ec2_resource_US_E = boto3.resource('ec2', region_name='us-east-1')


reservations_US_E = ec2_client_US_E.describe_instances()
instance_ids_US_E = []

for res in reservations_US_E["Reservations"]:
    instances = res["Instances"]
    for instance in instances:
        instance_ids_US_E.append(instance["InstanceId"])
        print(instance_ids_US_E)
        
response = ec2_resource_US_E.create_tags(
    Resources=instance_ids_US_E,
    Tags=[
        {
            'Key': 'Enviroment',
            'Value': 'Production'
        },
    ]
)
        
        
        
import boto3
import schedule
from operator import itemgetter

ec2_client = boto3.client('ec2', region_name='us-east-1')
ec2_resource = boto3.resource('ec2', region_name='us-east-1')

instance_id = "i-0dc4a530b63ac86dd"

volumes = ec2_client.describe_volumes(
    Filters=[
        {
            'Name': 'attachment.instance-id',
            'Values': [instance_id]
        }
    ]
)

instance_volumes = volumes["Volumes"][0]
print(instance_volumes)

snapshots = ec2_client.describe_snapshots(
    OwnerIds=['self'],
    Filters=[
        {
            'Name': 'volume-id',
            'Values': [instance_volumes["VolumeId"]]
        }
    ]
)

latest_snapshot = sorted(snapshots["Snapshots"], key=itemgetter('StartTime'), reverse=True)[0]
print(latest_snapshot["StartTime"])

new_volume = ec2_client.create_volume(
    AvailabilityZone=instance_volumes["AvailabilityZone"],
    SnapshotId=latest_snapshot["SnapshotId"],
    TagSpecifications=[
        {
            'ResourceType': 'volume',
            'Tags': [
                {
                    'Key': 'name',
                    'Value': 'prod'
                },
            ]
        },
    ]
)


while True:
    vol = ec2_resource.Volume(new_volume["VolumeId"])
    print(vol.state)
    if vol.state == "available":
        ec2_resource.Instance(instance_id).attach_volume(
            Device="/dev/xvdb",
            VolumeId=new_volume["VolumeId"]
        )
        break
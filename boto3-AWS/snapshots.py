import boto3
import schedule

ec2_client = boto3.client('ec2', region_name='us-east-1')


def create_snapshots():
    volumes = ec2_client.describe_volumes(
        filters=[
            {
                'Name': 'tag:name',
                'Values': ['prod']
            }
        ]
    )
    for volume in volumes["Volumes"]:
        new_snapshot = ec2_client.create_snapshot(
            Description='Snapshot of the volumes',
            VolumeId=volume["VolumeId"]
        )
        print(f"Snapshot {new_snapshot['SnapshotId']} is created for the volume {volume['VolumeId']}")
    
    
schedule.every().day.do(create_snapshots)

while True:
    schedule.run_pending()
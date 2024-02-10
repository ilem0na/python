import boto3
import schedule


ec2_client = boto3.client('ec2', region_name='us-east-1')
ec2_resource = boto3.resource('ec2', region_name='us-east-1')

all_available_vpcs = ec2_client.describe_vpcs()
vpcs = all_available_vpcs["Vpcs"]

reservations = ec2_client.describe_instances()
    
instances = reservations["Reservations"]
for instance in instances:
    print(instance["Instances"][0]['InstanceId'])
    print(instance["Instances"][0]['State']['Name'])
    
def check_instance_status():
    statuses = ec2_client.describe_instance_status(
        IncludeAllInstances=True
    )
    for status in statuses["InstanceStatuses"]:
        ins_status = status["InstanceStatus"]['Status']
        sys_status = status["SystemStatus"]["Status"]
        state = status["InstanceState"]
        print(f" Instance {status['InstanceId']} is with state:{state} with instance status: {ins_status} and system status: {sys_status}")
          

    
schedule.every(10).seconds.do(check_instance_status)
while True:
    schedule.run_pending()
    
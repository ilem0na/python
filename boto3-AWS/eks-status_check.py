import boto3

client = boto3.client('eks', region_name='us-east-1')

clusters = client.list_clusters()['clusters']

for cluster in clusters:
    cluster_info = client.describe_cluster(
        name=cluster
        )
    cluster_status = cluster_info['cluster']['status']
    cluster_endpoint = cluster_info['cluster']['endpoint']
    cluster_version = cluster_info['cluster']['version']
    print(f"Cluster {cluster} is in {cluster_status} state with the endpoint {cluster_endpoint} using {cluster_version}.")
#!/usr/bin/env python3
"""
AWS Infrastructure Cleanup Script - Python Version
Deletes all ECS, ALB, and related resources
"""

import boto3
import time
from botocore.exceptions import ClientError

# Configuration
CLUSTER_NAME = "devops-cluster"
SERVICE_NAME = "devops-service"
REGION = "us-east-1"
LOG_GROUP = "/ecs/devops-task"
SECURITY_GROUP_NAME = "devops-ecs-sg"
EXECUTION_ROLE_NAME = "ecsTaskExecutionRole"
ALB_NAME = "devops-alb"
TARGET_GROUP_NAME = "devops-targets"

def get_aws_clients():
    """Initialize AWS clients"""
    return {
        'ecs': boto3.client('ecs', region_name=REGION),
        'elbv2': boto3.client('elbv2', region_name=REGION),
        'ec2': boto3.client('ec2', region_name=REGION),
        'logs': boto3.client('logs', region_name=REGION),
        'iam': boto3.client('iam')
    }

def delete_ecs_service(ecs_client):
    """Delete ECS service"""
    print("Deleting ECS service...")
    try:
        # Scale service to 0
        ecs_client.update_service(
            cluster=CLUSTER_NAME,
            service=SERVICE_NAME,
            desiredCount=0
        )
        print("Scaled service to 0, waiting...")
        time.sleep(30)
        
        # Delete service
        ecs_client.delete_service(
            cluster=CLUSTER_NAME,
            service=SERVICE_NAME
        )
        print("ECS service deleted")
        
    except ClientError as e:
        if e.response['Error']['Code'] != 'ServiceNotFoundException':
            print(f"Error deleting ECS service: {e}")

def delete_ecs_cluster(ecs_client):
    """Delete ECS cluster"""
    print("Deleting ECS cluster...")
    try:
        ecs_client.delete_cluster(cluster=CLUSTER_NAME)
        print("ECS cluster deleted")
    except ClientError as e:
        if e.response['Error']['Code'] != 'ClusterNotFoundException':
            print(f"Error deleting ECS cluster: {e}")

def delete_alb_resources(elbv2_client):
    """Delete ALB and related resources"""
    print("Deleting ALB resources...")
    
    # Get ALB ARN
    try:
        response = elbv2_client.describe_load_balancers(Names=[ALB_NAME])
        if response['LoadBalancers']:
            alb_arn = response['LoadBalancers'][0]['LoadBalancerArn']
            
            # Delete listeners first
            try:
                listeners = elbv2_client.describe_listeners(LoadBalancerArn=alb_arn)
                for listener in listeners['Listeners']:
                    elbv2_client.delete_listener(ListenerArn=listener['ListenerArn'])
                    print("Deleted ALB listener")
            except ClientError as e:
                print(f"Error deleting listeners: {e}")
            
            # Delete ALB
            elbv2_client.delete_load_balancer(LoadBalancerArn=alb_arn)
            print("ALB deleted")
            
    except ClientError as e:
        if e.response['Error']['Code'] != 'LoadBalancerNotFound':
            print(f"Error deleting ALB: {e}")
    
    # Delete target group
    try:
        response = elbv2_client.describe_target_groups(Names=[TARGET_GROUP_NAME])
        if response['TargetGroups']:
            target_group_arn = response['TargetGroups'][0]['TargetGroupArn']
            elbv2_client.delete_target_group(TargetGroupArn=target_group_arn)
            print("Target group deleted")
    except ClientError as e:
        if e.response['Error']['Code'] != 'TargetGroupNotFound':
            print(f"Error deleting target group: {e}")

def delete_security_group(ec2_client):
    """Delete security group"""
    print("Deleting security group...")
    try:
        response = ec2_client.describe_security_groups(
            Filters=[{'Name': 'group-name', 'Values': [SECURITY_GROUP_NAME]}]
        )
        if response['SecurityGroups']:
            security_group_id = response['SecurityGroups'][0]['GroupId']
            ec2_client.delete_security_group(GroupId=security_group_id)
            print("Security group deleted")
    except ClientError as e:
        if e.response['Error']['Code'] not in ['InvalidGroupId.NotFound', 'InvalidGroup.NotFound']:
            print(f"Error deleting security group: {e}")

def delete_log_group(logs_client):
    """Delete CloudWatch log group"""
    print("Deleting CloudWatch log group...")
    try:
        logs_client.delete_log_group(logGroupName=LOG_GROUP)
        print("CloudWatch log group deleted")
    except ClientError as e:
        if e.response['Error']['Code'] != 'ResourceNotFoundException':
            print(f"Error deleting log group: {e}")

def delete_iam_role(iam_client):
    """Delete IAM role"""
    print("Deleting IAM role...")
    try:
        # Detach policy
        iam_client.detach_role_policy(
            RoleName=EXECUTION_ROLE_NAME,
            PolicyArn='arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy'
        )
        
        # Delete role
        iam_client.delete_role(RoleName=EXECUTION_ROLE_NAME)
        print("IAM role deleted")
        
    except ClientError as e:
        if e.response['Error']['Code'] != 'NoSuchEntity':
            print(f"Error deleting IAM role: {e}")

def main():
    """Main function"""
    print("Deleting AWS ECS infrastructure with Python...")
    
    # Initialize AWS clients
    clients = get_aws_clients()
    
    # Delete resources in order
    delete_ecs_service(clients['ecs'])
    delete_ecs_cluster(clients['ecs'])
    delete_alb_resources(clients['elbv2'])
    delete_security_group(clients['ec2'])
    delete_log_group(clients['logs'])
    delete_iam_role(clients['iam'])
    
    print("\nComplete cleanup finished!")
    print("Deleted: ECS Service, Cluster, ALB, Target Group, Security Group, Log Group, IAM Role")

if __name__ == "__main__":
    main()
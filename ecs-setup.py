#!/usr/bin/env python3
"""
AWS ECS Infrastructure Setup Script - Python Version
Creates ECS cluster, IAM roles, security groups, and CloudWatch log groups
"""

import boto3
import json
import sys
import time
from botocore.exceptions import ClientError

# Configuration
CLUSTER_NAME = "devops-cluster"
SERVICE_NAME = "devops-service"
TASK_DEFINITION = "devops-task"
REGION = "us-east-1"
LOG_GROUP = "/ecs/devops-task"
SECURITY_GROUP_NAME = "devops-ecs-sg"
EXECUTION_ROLE_NAME = "ecsTaskExecutionRole"

def get_aws_clients():
    """Initialize AWS clients"""
    return {
        'ecs': boto3.client('ecs', region_name=REGION),
        'ec2': boto3.client('ec2', region_name=REGION),
        'logs': boto3.client('logs', region_name=REGION),
        'iam': boto3.client('iam'),
        'sts': boto3.client('sts')
    }

def get_account_id(sts_client):
    """Get AWS Account ID"""
    try:
        return sts_client.get_caller_identity()['Account']
    except ClientError as e:
        print(f"Error getting account ID: {e}")
        return None

def check_iam_role_exists(iam_client, role_name):
    """Check if IAM role exists"""
    try:
        iam_client.get_role(RoleName=role_name)
        return True
    except ClientError:
        return False

def create_iam_role(iam_client):
    """Create ECS Task Execution Role"""
    if check_iam_role_exists(iam_client, EXECUTION_ROLE_NAME):
        print(f"ECS Task Execution Role '{EXECUTION_ROLE_NAME}' already exists")
        return True
    
    print(f"Creating ECS Task Execution Role '{EXECUTION_ROLE_NAME}'...")
    
    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {"Service": "ecs-tasks.amazonaws.com"},
                "Action": "sts:AssumeRole"
            }
        ]
    }
    
    try:
        # Create role
        iam_client.create_role(
            RoleName=EXECUTION_ROLE_NAME,
            AssumeRolePolicyDocument=json.dumps(trust_policy)
        )
        
        # Attach policy
        iam_client.attach_role_policy(
            RoleName=EXECUTION_ROLE_NAME,
            PolicyArn='arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy'
        )
        
        print("Waiting for role to be available...")
        time.sleep(10)
        return True
        
    except ClientError as e:
        print(f"Error creating IAM role: {e}")
        return False

def check_cluster_exists(ecs_client, cluster_name):
    """Check if ECS cluster exists"""
    try:
        response = ecs_client.describe_clusters(clusters=[cluster_name])
        clusters = response.get('clusters', [])
        return len(clusters) > 0 and clusters[0]['status'] == 'ACTIVE'
    except ClientError:
        return False

def create_ecs_cluster(ecs_client):
    """Create ECS cluster"""
    if check_cluster_exists(ecs_client, CLUSTER_NAME):
        print(f"ECS cluster '{CLUSTER_NAME}' already exists")
        return True
    
    print(f"Creating ECS cluster '{CLUSTER_NAME}'...")
    try:
        ecs_client.create_cluster(clusterName=CLUSTER_NAME)
        return True
    except ClientError as e:
        print(f"Error creating ECS cluster: {e}")
        return False

def check_log_group_exists(logs_client, log_group_name):
    """Check if CloudWatch log group exists"""
    try:
        response = logs_client.describe_log_groups(logGroupNamePrefix=log_group_name)
        return any(lg['logGroupName'] == log_group_name for lg in response.get('logGroups', []))
    except ClientError:
        return False

def create_log_group(logs_client):
    """Create CloudWatch log group"""
    if check_log_group_exists(logs_client, LOG_GROUP):
        print(f"CloudWatch log group '{LOG_GROUP}' already exists")
        return True
    
    print(f"Creating CloudWatch log group '{LOG_GROUP}'...")
    try:
        logs_client.create_log_group(logGroupName=LOG_GROUP)
        return True
    except ClientError as e:
        print(f"Error creating log group: {e}")
        return False

def get_default_vpc_info(ec2_client):
    """Get default VPC and subnet information"""
    try:
        # Get default VPC
        vpcs = ec2_client.describe_vpcs(Filters=[{'Name': 'is-default', 'Values': ['true']}])
        if not vpcs['Vpcs']:
            print("No default VPC found")
            return None, None
        
        vpc_id = vpcs['Vpcs'][0]['VpcId']
        
        # Get subnets
        subnets = ec2_client.describe_subnets(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])
        subnet_ids = [subnet['SubnetId'] for subnet in subnets['Subnets'][:2]]
        
        return vpc_id, subnet_ids
        
    except ClientError as e:
        print(f"Error getting VPC info: {e}")
        return None, None

def check_security_group_exists(ec2_client, group_name):
    """Check if security group exists"""
    try:
        response = ec2_client.describe_security_groups(
            Filters=[{'Name': 'group-name', 'Values': [group_name]}]
        )
        return len(response['SecurityGroups']) > 0
    except ClientError:
        return False

def create_security_group(ec2_client, vpc_id):
    """Create security group"""
    if check_security_group_exists(ec2_client, SECURITY_GROUP_NAME):
        print(f"Security group '{SECURITY_GROUP_NAME}' already exists")
        return True
    
    print(f"Creating security group '{SECURITY_GROUP_NAME}'...")
    try:
        # Create security group
        response = ec2_client.create_security_group(
            GroupName=SECURITY_GROUP_NAME,
            Description='Security group for DevOps ECS service',
            VpcId=vpc_id
        )
        security_group_id = response['GroupId']
        
        # Add inbound rules
        ec2_client.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=[
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 3000,
                    'ToPort': 3000,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                },
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 80,
                    'ToPort': 80,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                }
            ]
        )
        
        return True
        
    except ClientError as e:
        print(f"Error creating security group: {e}")
        return False

def main():
    """Main function"""
    print("Setting up AWS ECS infrastructure with Python...")
    
    # Initialize AWS clients
    clients = get_aws_clients()
    
    # Get account ID
    account_id = get_account_id(clients['sts'])
    if not account_id:
        sys.exit(1)
    
    # Get VPC info
    vpc_id, subnet_ids = get_default_vpc_info(clients['ec2'])
    if not vpc_id:
        sys.exit(1)
    
    # Create resources
    success = True
    success &= create_iam_role(clients['iam'])
    success &= create_ecs_cluster(clients['ecs'])
    success &= create_log_group(clients['logs'])
    success &= create_security_group(clients['ec2'], vpc_id)
    
    if success:
        print("\nECS infrastructure setup completed!")
        print(f"Account ID: {account_id}")
        print(f"Execution Role: arn:aws:iam::{account_id}:role/{EXECUTION_ROLE_NAME}")
        print(f"Cluster: {CLUSTER_NAME}")
        print(f"Log Group: {LOG_GROUP}")
        print(f"VPC ID: {vpc_id}")
        print(f"Subnet IDs: {', '.join(subnet_ids)}")
    else:
        print("Some resources failed to create. Check the logs above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
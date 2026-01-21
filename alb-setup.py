#!/usr/bin/env python3
"""
AWS Application Load Balancer Setup Script - Python Version
Creates ALB, target groups, and listeners for fixed endpoint
"""

import boto3
import sys
from botocore.exceptions import ClientError

# Configuration
REGION = "us-east-1"
ALB_NAME = "devops-alb"
TARGET_GROUP_NAME = "devops-targets"

def get_aws_clients():
    """Initialize AWS clients"""
    return {
        'elbv2': boto3.client('elbv2', region_name=REGION),
        'ec2': boto3.client('ec2', region_name=REGION)
    }

def get_vpc_and_subnets(ec2_client):
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

def get_security_group_id(ec2_client):
    """Get security group ID"""
    try:
        response = ec2_client.describe_security_groups(
            Filters=[{'Name': 'group-name', 'Values': ['devops-ecs-sg']}]
        )
        if response['SecurityGroups']:
            return response['SecurityGroups'][0]['GroupId']
        else:
            print("Security group 'devops-ecs-sg' not found")
            return None
    except ClientError as e:
        print(f"Error getting security group: {e}")
        return None

def check_target_group_exists(elbv2_client, target_group_name):
    """Check if target group exists"""
    try:
        response = elbv2_client.describe_target_groups(Names=[target_group_name])
        return len(response['TargetGroups']) > 0
    except ClientError:
        return False

def create_target_group(elbv2_client, vpc_id):
    """Create target group"""
    if check_target_group_exists(elbv2_client, TARGET_GROUP_NAME):
        print(f"Target group '{TARGET_GROUP_NAME}' already exists")
        # Get existing target group ARN
        response = elbv2_client.describe_target_groups(Names=[TARGET_GROUP_NAME])
        return response['TargetGroups'][0]['TargetGroupArn']
    
    print(f"Creating target group '{TARGET_GROUP_NAME}'...")
    try:
        response = elbv2_client.create_target_group(
            Name=TARGET_GROUP_NAME,
            Protocol='HTTP',
            Port=3000,
            VpcId=vpc_id,
            TargetType='ip',
            HealthCheckPath='/',
            HealthCheckProtocol='HTTP',
            HealthCheckPort='3000'
        )
        return response['TargetGroups'][0]['TargetGroupArn']
        
    except ClientError as e:
        print(f"Error creating target group: {e}")
        return None

def check_load_balancer_exists(elbv2_client, alb_name):
    """Check if load balancer exists"""
    try:
        response = elbv2_client.describe_load_balancers(Names=[alb_name])
        return len(response['LoadBalancers']) > 0
    except ClientError:
        return False

def create_load_balancer(elbv2_client, subnet_ids, security_group_id):
    """Create Application Load Balancer"""
    if check_load_balancer_exists(elbv2_client, ALB_NAME):
        print(f"Application Load Balancer '{ALB_NAME}' already exists")
        # Get existing ALB ARN
        response = elbv2_client.describe_load_balancers(Names=[ALB_NAME])
        return response['LoadBalancers'][0]['LoadBalancerArn']
    
    print(f"Creating Application Load Balancer '{ALB_NAME}'...")
    try:
        response = elbv2_client.create_load_balancer(
            Name=ALB_NAME,
            Subnets=subnet_ids,
            SecurityGroups=[security_group_id],
            Scheme='internet-facing',
            Type='application',
            IpAddressType='ipv4'
        )
        return response['LoadBalancers'][0]['LoadBalancerArn']
        
    except ClientError as e:
        print(f"Error creating load balancer: {e}")
        return None

def check_listener_exists(elbv2_client, load_balancer_arn):
    """Check if listener exists"""
    try:
        response = elbv2_client.describe_listeners(LoadBalancerArn=load_balancer_arn)
        return len(response['Listeners']) > 0
    except ClientError:
        return False

def create_listener(elbv2_client, load_balancer_arn, target_group_arn):
    """Create ALB listener"""
    if check_listener_exists(elbv2_client, load_balancer_arn):
        print("ALB listener already exists")
        return True
    
    print("Creating ALB listener...")
    try:
        elbv2_client.create_listener(
            LoadBalancerArn=load_balancer_arn,
            Protocol='HTTP',
            Port=80,
            DefaultActions=[
                {
                    'Type': 'forward',
                    'TargetGroupArn': target_group_arn
                }
            ]
        )
        return True
        
    except ClientError as e:
        print(f"Error creating listener: {e}")
        return False

def get_alb_dns_name(elbv2_client, load_balancer_arn):
    """Get ALB DNS name"""
    try:
        response = elbv2_client.describe_load_balancers(LoadBalancerArns=[load_balancer_arn])
        return response['LoadBalancers'][0]['DNSName']
    except ClientError as e:
        print(f"Error getting ALB DNS name: {e}")
        return None

def main():
    """Main function"""
    print("Setting up Application Load Balancer with Python...")
    
    # Initialize AWS clients
    clients = get_aws_clients()
    
    # Get VPC and subnet info
    vpc_id, subnet_ids = get_vpc_and_subnets(clients['ec2'])
    if not vpc_id or not subnet_ids:
        sys.exit(1)
    
    # Get security group
    security_group_id = get_security_group_id(clients['ec2'])
    if not security_group_id:
        sys.exit(1)
    
    # Create target group
    target_group_arn = create_target_group(clients['elbv2'], vpc_id)
    if not target_group_arn:
        sys.exit(1)
    
    # Create load balancer
    load_balancer_arn = create_load_balancer(clients['elbv2'], subnet_ids, security_group_id)
    if not load_balancer_arn:
        sys.exit(1)
    
    # Create listener
    if not create_listener(clients['elbv2'], load_balancer_arn, target_group_arn):
        sys.exit(1)
    
    # Get ALB DNS name
    alb_dns = get_alb_dns_name(clients['elbv2'], load_balancer_arn)
    
    print("\nALB setup completed!")
    print(f"ALB DNS: {alb_dns}")
    print(f"Target Group ARN: {target_group_arn}")
    print(f"Access your app at: http://{alb_dns}")

if __name__ == "__main__":
    main()
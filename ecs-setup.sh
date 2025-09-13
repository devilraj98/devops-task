#!/bin/bash

# ECS Setup Script
echo "Setting up AWS ECS resources..."

# Variables
CLUSTER_NAME="devops-cluster"
SERVICE_NAME="devops-service"
TASK_DEFINITION="devops-task"
REGION="us-east-1"

# Create ECS cluster
echo "Creating ECS cluster..."
aws ecs create-cluster --cluster-name $CLUSTER_NAME --region $REGION

# Create CloudWatch log group
echo "Creating CloudWatch log group..."
aws logs create-log-group --log-group-name "/ecs/devops-task" --region $REGION

# Register task definition
echo "Registering task definition..."
aws ecs register-task-definition --cli-input-json file://task-definition.json --region $REGION

# Get default VPC and subnets
echo "Getting VPC and subnet information..."
VPC_ID=$(aws ec2 describe-vpcs --filters "Name=is-default,Values=true" --query "Vpcs[0].VpcId" --output text --region $REGION)
SUBNET_IDS=$(aws ec2 describe-subnets --filters "Name=vpc-id,Values=$VPC_ID" --query "Subnets[0:2].SubnetId" --output text --region $REGION)

# Create security group
echo "Creating security group..."
SECURITY_GROUP_ID=$(aws ec2 create-security-group \
    --group-name devops-ecs-sg \
    --description "Security group for DevOps ECS service" \
    --vpc-id $VPC_ID \
    --region $REGION \
    --query "GroupId" --output text)

# Add inbound rule for port 3000
aws ec2 authorize-security-group-ingress \
    --group-id $SECURITY_GROUP_ID \
    --protocol tcp \
    --port 3000 \
    --cidr 0.0.0.0/0 \
    --region $REGION

echo "ECS resources created successfully!"
echo "Cluster: $CLUSTER_NAME"
echo "Security Group: $SECURITY_GROUP_ID"
echo "Subnets: $SUBNET_IDS"
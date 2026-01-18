#!/bin/bash

# ECS Setup Script - Idempotent version for CI/CD
echo "Setting up AWS ECS resources..."

# Variables
CLUSTER_NAME="devops-cluster"
SERVICE_NAME="devops-service"
TASK_DEFINITION="devops-task"
REGION="us-east-1"
LOG_GROUP="/ecs/devops-task"
SECURITY_GROUP_NAME="devops-ecs-sg"
EXECUTION_ROLE_NAME="ecsTaskExecutionRole"

# Get AWS Account ID
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

# Function to check if resource exists
check_cluster() {
    aws ecs describe-clusters --clusters $CLUSTER_NAME --region $REGION --query 'clusters[0].status' --output text 2>/dev/null
}

check_log_group() {
    aws logs describe-log-groups --log-group-name-prefix $LOG_GROUP --region $REGION --query 'logGroups[0].logGroupName' --output text 2>/dev/null
}

check_security_group() {
    aws ec2 describe-security-groups --filters "Name=group-name,Values=$SECURITY_GROUP_NAME" --query 'SecurityGroups[0].GroupId' --output text --region $REGION 2>/dev/null
}

check_iam_role() {
    aws iam get-role --role-name $EXECUTION_ROLE_NAME --query 'Role.RoleName' --output text 2>/dev/null
}

# Create ECS Task Execution Role if it doesn't exist
echo "Checking ECS Task Execution Role..."
if [ "$(check_iam_role)" != "$EXECUTION_ROLE_NAME" ]; then
    echo "Creating ECS Task Execution Role..."
    
    # Create trust policy
    cat > trust-policy.json << EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "ecs-tasks.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
    
    # Create the role
    aws iam create-role \
        --role-name $EXECUTION_ROLE_NAME \
        --assume-role-policy-document file://trust-policy.json
    
    # Attach the AWS managed policy
    aws iam attach-role-policy \
        --role-name $EXECUTION_ROLE_NAME \
        --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy
    
    # Clean up temp file
    rm trust-policy.json
    
    echo "Waiting for role to be available..."
    sleep 10
else
    echo "ECS Task Execution Role already exists"
fi

# Create ECS cluster if it doesn't exist
echo "Checking ECS cluster..."
if [ "$(check_cluster)" != "ACTIVE" ]; then
    echo "Creating ECS cluster..."
    aws ecs create-cluster --cluster-name $CLUSTER_NAME --region $REGION
else
    echo "ECS cluster already exists"
fi

# Create CloudWatch log group if it doesn't exist
echo "Checking CloudWatch log group..."
if [ "$(check_log_group)" != "$LOG_GROUP" ]; then
    echo "Creating CloudWatch log group..."
    aws logs create-log-group --log-group-name $LOG_GROUP --region $REGION
else
    echo "CloudWatch log group already exists"
fi

# Get default VPC and subnets
echo "Getting VPC and subnet information..."
VPC_ID=$(aws ec2 describe-vpcs --filters "Name=is-default,Values=true" --query "Vpcs[0].VpcId" --output text --region $REGION)
SUBNET_IDS=$(aws ec2 describe-subnets --filters "Name=vpc-id,Values=$VPC_ID" --query "Subnets[0:2].SubnetId" --output text --region $REGION)

# Create security group if it doesn't exist
echo "Checking security group..."
SECURITY_GROUP_ID=$(check_security_group)
if [ "$SECURITY_GROUP_ID" = "None" ] || [ -z "$SECURITY_GROUP_ID" ]; then
    echo "Creating security group..."
    SECURITY_GROUP_ID=$(aws ec2 create-security-group \
        --group-name $SECURITY_GROUP_NAME \
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
else
    echo "Security group already exists: $SECURITY_GROUP_ID"
fi

echo "ECS infrastructure setup completed!"
echo "Account ID: $ACCOUNT_ID"
echo "Execution Role: arn:aws:iam::$ACCOUNT_ID:role/$EXECUTION_ROLE_NAME"
echo "Cluster: $CLUSTER_NAME"
echo "Security Group: $SECURITY_GROUP_ID"
echo "Subnets: $SUBNET_IDS"
echo "Log Group: $LOG_GROUP"
#!/bin/bash

# ALB Setup Script for Fixed Endpoint
echo "Setting up Application Load Balancer..."

REGION="us-east-1"
ALB_NAME="devops-alb"
TARGET_GROUP_NAME="devops-targets"

# Get VPC and subnets
VPC_ID=$(aws ec2 describe-vpcs --filters "Name=is-default,Values=true" --query "Vpcs[0].VpcId" --output text --region $REGION)
SUBNET_IDS=$(aws ec2 describe-subnets --filters "Name=vpc-id,Values=$VPC_ID" --query "Subnets[0:2].SubnetId" --output text --region $REGION)

# Get security group
SECURITY_GROUP_ID=$(aws ec2 describe-security-groups --filters "Name=group-name,Values=devops-ecs-sg" --query "SecurityGroups[0].GroupId" --output text --region $REGION)

# Create target group
echo "Creating target group..."
TARGET_GROUP_ARN=$(aws elbv2 create-target-group \
    --name $TARGET_GROUP_NAME \
    --protocol HTTP \
    --port 3000 \
    --vpc-id $VPC_ID \
    --target-type ip \
    --health-check-path / \
    --region $REGION \
    --query 'TargetGroups[0].TargetGroupArn' --output text)

# Create ALB
echo "Creating Application Load Balancer..."
ALB_ARN=$(aws elbv2 create-load-balancer \
    --name $ALB_NAME \
    --subnets $SUBNET_IDS \
    --security-groups $SECURITY_GROUP_ID \
    --region $REGION \
    --query 'LoadBalancers[0].LoadBalancerArn' --output text)

# Create listener
echo "Creating ALB listener..."
aws elbv2 create-listener \
    --load-balancer-arn $ALB_ARN \
    --protocol HTTP \
    --port 80 \
    --default-actions Type=forward,TargetGroupArn=$TARGET_GROUP_ARN \
    --region $REGION

# Get ALB DNS name
ALB_DNS=$(aws elbv2 describe-load-balancers --load-balancer-arns $ALB_ARN --query 'LoadBalancers[0].DNSName' --output text --region $REGION)

echo "ALB setup completed!"
echo "ALB DNS: $ALB_DNS"
echo "Target Group ARN: $TARGET_GROUP_ARN"
echo "Access your app at: http://$ALB_DNS"
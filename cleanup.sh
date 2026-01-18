#!/bin/bash

# ECS Infrastructure Cleanup Script
echo "Deleting AWS ECS infrastructure..."

CLUSTER_NAME="devops-cluster"
SERVICE_NAME="devops-service"
REGION="us-east-1"
LOG_GROUP="/ecs/devops-task"
SECURITY_GROUP_NAME="devops-ecs-sg"
EXECUTION_ROLE_NAME="ecsTaskExecutionRole"

# Delete ECS Service
echo "Deleting ECS service..."
aws ecs update-service --cluster $CLUSTER_NAME --service $SERVICE_NAME --desired-count 0 --region $REGION 2>/dev/null
aws ecs delete-service --cluster $CLUSTER_NAME --service $SERVICE_NAME --region $REGION 2>/dev/null

# Delete ECS Cluster
echo "Deleting ECS cluster..."
aws ecs delete-cluster --cluster $CLUSTER_NAME --region $REGION 2>/dev/null

# Delete Security Group
echo "Deleting security group..."
SECURITY_GROUP_ID=$(aws ec2 describe-security-groups --filters "Name=group-name,Values=$SECURITY_GROUP_NAME" --query 'SecurityGroups[0].GroupId' --output text --region $REGION 2>/dev/null)
if [ "$SECURITY_GROUP_ID" != "None" ] && [ -n "$SECURITY_GROUP_ID" ]; then
    aws ec2 delete-security-group --group-id $SECURITY_GROUP_ID --region $REGION 2>/dev/null
fi

# Delete CloudWatch Log Group
echo "Deleting CloudWatch log group..."
aws logs delete-log-group --log-group-name $LOG_GROUP --region $REGION 2>/dev/null

# Delete IAM Role
echo "Deleting IAM role..."
aws iam detach-role-policy --role-name $EXECUTION_ROLE_NAME --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy 2>/dev/null
aws iam delete-role --role-name $EXECUTION_ROLE_NAME 2>/dev/null

echo "Cleanup completed!"
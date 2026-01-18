#!/bin/bash

# Complete Infrastructure Cleanup Script
echo "Deleting AWS ECS infrastructure with ALB..."

CLUSTER_NAME="devops-cluster"
SERVICE_NAME="devops-service"
REGION="us-east-1"
LOG_GROUP="/ecs/devops-task"
SECURITY_GROUP_NAME="devops-ecs-sg"
EXECUTION_ROLE_NAME="ecsTaskExecutionRole"
ALB_NAME="devops-alb"
TARGET_GROUP_NAME="devops-targets"

# Delete ECS Service
echo "Deleting ECS service..."
aws ecs update-service --cluster $CLUSTER_NAME --service $SERVICE_NAME --desired-count 0 --region $REGION 2>/dev/null
aws ecs delete-service --cluster $CLUSTER_NAME --service $SERVICE_NAME --region $REGION 2>/dev/null

# Delete ECS Cluster
echo "Deleting ECS cluster..."
aws ecs delete-cluster --cluster $CLUSTER_NAME --region $REGION 2>/dev/null

# Delete ALB and Target Group
echo "Deleting ALB resources..."
ALB_ARN=$(aws elbv2 describe-load-balancers --names $ALB_NAME --query 'LoadBalancers[0].LoadBalancerArn' --output text --region $REGION 2>/dev/null)
if [ "$ALB_ARN" != "None" ] && [ -n "$ALB_ARN" ]; then
    # Delete listeners first
    LISTENER_ARNS=$(aws elbv2 describe-listeners --load-balancer-arn $ALB_ARN --query 'Listeners[].ListenerArn' --output text --region $REGION 2>/dev/null)
    for LISTENER_ARN in $LISTENER_ARNS; do
        aws elbv2 delete-listener --listener-arn $LISTENER_ARN --region $REGION 2>/dev/null
    done
    
    # Delete ALB
    aws elbv2 delete-load-balancer --load-balancer-arn $ALB_ARN --region $REGION 2>/dev/null
fi

# Delete Target Group
TARGET_GROUP_ARN=$(aws elbv2 describe-target-groups --names $TARGET_GROUP_NAME --query 'TargetGroups[0].TargetGroupArn' --output text --region $REGION 2>/dev/null)
if [ "$TARGET_GROUP_ARN" != "None" ] && [ -n "$TARGET_GROUP_ARN" ]; then
    aws elbv2 delete-target-group --target-group-arn $TARGET_GROUP_ARN --region $REGION 2>/dev/null
fi

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

echo "Complete cleanup finished!"
echo "Deleted: ECS Service, Cluster, ALB, Target Group, Security Group, Log Group, IAM Role"
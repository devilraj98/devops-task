#!/bin/bash

echo "Setting up CloudWatch monitoring..."

# Create CloudWatch dashboard
aws cloudwatch put-dashboard \
    --dashboard-name "DevOps-Task-Dashboard" \
    --dashboard-body file://cloudwatch-dashboard.json \
    --region us-east-1

# Create CloudWatch alarm for high CPU
aws cloudwatch put-metric-alarm \
    --alarm-name "DevOps-Task-High-CPU" \
    --alarm-description "Alarm when CPU exceeds 80%" \
    --metric-name CPUUtilization \
    --namespace AWS/ECS \
    --statistic Average \
    --period 300 \
    --threshold 80 \
    --comparison-operator GreaterThanThreshold \
    --dimensions Name=ServiceName,Value=devops-service Name=ClusterName,Value=devops-cluster \
    --evaluation-periods 2 \
    --region us-east-1

echo "✅ CloudWatch dashboard and alarms created successfully!"
echo "📊 Dashboard: https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#dashboards:name=DevOps-Task-Dashboard"
echo "📋 Logs: https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#logsV2:log-groups/log-group/%2Fecs%2Fdevops-task"
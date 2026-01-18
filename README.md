# DevOps CI/CD Pipeline Project

A complete CI/CD pipeline implementation for a Node.js application using Jenkins, Docker, AWS ECS, Application Load Balancer, and CloudWatch monitoring.

## 🏗️ Architecture Diagram

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Developer     │    │     GitHub      │    │    Jenkins      │
│                 │───▶│   Repository    │───▶│   CI/CD Server  │
│  Local Machine  │    │  (main/dev)     │    │   (EC2 Instance)│
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
                                                        ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   CloudWatch    │    │   AWS ECS       │    │   DockerHub     │
│   Monitoring    │◀───│   Container     │◀───│   Registry      │
│   & Logging     │    │   Service       │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                        ▲
                                ▼                        │
                       ┌─────────────────┐    ┌─────────────────┐
                       │ Application     │    │ Infrastructure  │
                       │ Load Balancer   │    │ Automation      │
                       │ (Fixed Endpoint)│    │ (IAM Roles)     │
                       └─────────────────┘    └─────────────────┘
```

## 📋 Project Overview

This project demonstrates a complete DevOps CI/CD pipeline with:
- **Source Control**: GitHub with branching strategy (main/dev)
- **CI/CD**: Jenkins pipeline with automated builds
- **Infrastructure Automation**: Automated AWS resource provisioning
- **Containerization**: Docker with multi-stage builds
- **Registry**: DockerHub for image storage
- **Deployment**: AWS ECS (Fargate) for container orchestration
- **Load Balancing**: Application Load Balancer for fixed endpoint
- **Monitoring**: CloudWatch for logs and metrics
- **Security**: Automated IAM role creation and management

## 🚀 Pipeline Flow

### 1. Infrastructure Setup (NEW)
- Automated AWS ECS cluster creation
- IAM role provisioning with proper permissions
- Application Load Balancer setup for fixed endpoint
- Security group and VPC configuration
- CloudWatch log group creation

### 2. Code Commit
- Developer pushes code to `dev` branch
- GitHub webhook triggers Jenkins pipeline

### 3. Build Stage
- Install Node.js dependencies (`npm install`)
- Run automated tests (`npm test`)
- Validate application structure

### 4. Dockerize Stage
- Build Docker image with application
- Tag image with build number
- Create latest tag for deployment

### 5. Push to Registry
- Authenticate with DockerHub
- Push tagged images to registry
- Images available for deployment

### 6. Deploy Stage (ENHANCED)
- Dynamic account ID detection
- Register new task definition with updated image
- Create or update ECS service with ALB integration
- Zero-downtime deployment with health checks
- Display fixed ALB endpoint

### 7. Monitoring
- CloudWatch logs collection
- CPU/Memory metrics monitoring
- Automated alerts for issues

## 🛠️ Setup Instructions

### Prerequisites
- AWS Account with appropriate permissions
- DockerHub account
- GitHub repository
- EC2 instance for Jenkins

### 1. Infrastructure Setup (FULLY AUTOMATED)

```bash
# Clone repository
git clone https://github.com/devilraj98/devops-task.git
cd devops-task

# Infrastructure is now automatically created by Jenkins pipeline!
# No manual setup required - just run the pipeline
```

**What gets created automatically:**
- ECS Cluster (`devops-cluster`)
- IAM Execution Role (`ecsTaskExecutionRole`)
- Application Load Balancer (`devops-alb`)
- Target Group (`devops-targets`)
- Security Group (`devops-ecs-sg`)
- CloudWatch Log Group (`/ecs/devops-task`)

### 2. Jenkins Configuration

1. **Install Jenkins on EC2**
   ```bash
   # Install Java, Jenkins, Docker, Node.js, AWS CLI
   # Configure security groups (ports 8080, 80)
   ```

2. **Install Required Plugins**
   - Docker Pipeline
   - GitHub Integration
   - NodeJS Plugin
   - AWS Credentials Plugin

3. **Configure Credentials**
   - DockerHub credentials (`dockerhub-credentials`)
   - AWS credentials (`aws-credentials`) with IAM permissions

4. **Create Pipeline Job**
   - Repository: `https://github.com/devilraj98/devops-task.git`
   - Branch: `*/dev`
   - Pipeline script from SCM

### 3. GitHub Webhook Setup

1. Repository Settings → Webhooks
2. Payload URL: `http://your-jenkins-ip:8080/github-webhook/`
3. Content type: `application/json`
4. Events: Push events

### 4. Required AWS IAM Permissions

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ecs:*",
                "ec2:*",
                "elbv2:*",
                "logs:*",
                "iam:CreateRole",
                "iam:GetRole",
                "iam:AttachRolePolicy",
                "sts:GetCallerIdentity"
            ],
            "Resource": "*"
        }
    ]
}
```

## 📁 Project Structure

```
devops-task/
├── app.js                    # Main Node.js application
├── package.json              # Dependencies and scripts
├── test.js                   # Automated tests
├── Dockerfile                # Container configuration
├── .dockerignore            # Docker build exclusions
├── Jenkinsfile              # CI/CD pipeline definition
├── task-definition.json     # ECS task configuration
├── service-definition.json  # ECS service with ALB config (NEW)
├── ecs-setup.sh            # AWS ECS setup script (ENHANCED)
├── alb-setup.sh            # Application Load Balancer setup (NEW)
├── cleanup.sh              # Complete infrastructure cleanup (NEW)
├── setup-monitoring.sh     # CloudWatch setup script
├── cloudwatch-dashboard.json # Monitoring dashboard
└── README.md               # This documentation
```

## 🔧 Configuration Files

### Jenkinsfile Pipeline Stages (UPDATED)
- **Infrastructure Setup**: Automated AWS resource provisioning (NEW)
- **Build**: Dependencies installation and testing
- **Dockerize**: Container image creation
- **Push**: Registry upload
- **Deploy**: ECS service with ALB integration (ENHANCED)

### ECS Task Definition
- **CPU**: 256 units (0.25 vCPU)
- **Memory**: 512 MB
- **Network**: awsvpc mode
- **Launch Type**: Fargate
- **Dynamic Account ID**: Auto-detects AWS account (NEW)

### Application Load Balancer (NEW)
- **Protocol**: HTTP
- **Port**: 80 (public access)
- **Target Port**: 3000 (container port)
- **Health Checks**: Automated container health monitoring
- **Fixed Endpoint**: DNS name never changes

## 📊 Monitoring & Logging

### CloudWatch Dashboard
- **Metrics**: CPU utilization, Memory usage
- **Logs**: Application logs with timestamps
- **Alarms**: High CPU usage alerts

### Access Monitoring
- **Dashboard**: [CloudWatch Console](https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#dashboards:name=DevOps-Task-Dashboard)
- **Logs**: [CloudWatch Logs](https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#logsV2:log-groups/log-group/%2Fecs%2Fdevops-task)

## 🌐 Application Access (FIXED ENDPOINT)

After successful deployment:
- **Fixed URL**: `http://devops-alb-XXXXXXXXX.us-east-1.elb.amazonaws.com`
- **Port**: 80 (standard HTTP)
- **No More IP Changes**: ALB provides permanent endpoint
- **Zero Downtime**: Seamless deployments without service interruption

### How to Get Your ALB Endpoint:
1. **From Jenkins Console**: Check deployment stage output
2. **AWS Console**: EC2 → Load Balancers → devops-alb → DNS name
3. **AWS CLI**: 
   ```bash
   aws elbv2 describe-load-balancers --names devops-alb --query 'LoadBalancers[0].DNSName' --output text
   ```

## 🧹 Infrastructure Cleanup (AUTOMATED)

### Complete Cleanup Script
```bash
# Make cleanup script executable
chmod +x cleanup.sh

# Delete all infrastructure
./cleanup.sh
```

### What Gets Deleted:
- ECS Service and Cluster
- Application Load Balancer and Target Group
- Security Groups
- CloudWatch Log Groups
- IAM Roles and Policies

### Jenkins Cleanup Pipeline
Create a separate Jenkins job for cleanup:
```groovy
pipeline {
    agent any
    environment {
        AWS_CREDENTIALS = credentials('aws-credentials')
        AWS_DEFAULT_REGION = 'us-east-1'
    }
    stages {
        stage('Checkout') {
            steps {
                git branch: 'dev', url: 'https://github.com/devilraj98/devops-task.git'
            }
        }
        stage('Cleanup') {
            steps {
                sh '''
                    chmod +x cleanup.sh
                    ./cleanup.sh
                '''
            }
        }
    }
}
```

## 🔄 Branching Strategy

- **main**: Production-ready code
- **dev**: Development and testing
- **Workflow**: Feature → dev → Pull Request → main

## 🚨 Troubleshooting

### Common Issues
1. **Jenkins Build Fails**: Check Node.js tool configuration
2. **Docker Push Denied**: Verify DockerHub credentials
3. **Docker Push Denied**: Jenkins user not added to Docker group
4. **ECS Deployment Fails**: Check AWS credentials and permissions
5. **IAM Role Error**: Ensure AWS credentials have IAM permissions
6. **ALB Not Created**: Check VPC and subnet availability
7. **Webhook Not Triggering**: Verify GitHub webhook URL
8. **Service Won't Start**: Check ALB target group health checks

### Logs Location
- **Jenkins**: Build console output
- **Docker**: Container logs via `docker logs`
- **ECS**: CloudWatch logs `/ecs/devops-task`
- **ALB**: Access logs (if enabled)

### Debug Commands
```bash
# Check ECS service status
aws ecs describe-services --cluster devops-cluster --services devops-service

# Check ALB health
aws elbv2 describe-target-health --target-group-arn <TARGET_GROUP_ARN>

# View application logs
aws logs tail /ecs/devops-task --follow
```

## 📈 Best Practices Implemented

- ✅ **Automated Infrastructure Provisioning** (NEW)
- ✅ **Fixed Application Endpoint with ALB** (NEW)
- ✅ **Dynamic Account ID Detection** (NEW)
- ✅ **Idempotent Infrastructure Scripts** (NEW)
- ✅ **Complete Cleanup Automation** (NEW)
- ✅ Automated testing in CI pipeline
- ✅ Multi-stage Docker builds
- ✅ Infrastructure as Code (ECS task definitions)
- ✅ Monitoring and alerting
- ✅ Zero-downtime deployments
- ✅ Proper branching strategy
- ✅ Security best practices (credentials management)

## 🎯 Future Enhancements

- [ ] **HTTPS/SSL Certificate Integration**
- [ ] **Auto Scaling based on CPU/Memory metrics**
- [ ] **Blue-Green deployment strategy**
- [ ] **Multi-AZ deployment for high availability**
- [ ] Terraform for complete Infrastructure as Code
- [ ] Automated rollback on failure
- [ ] Security scanning in pipeline
- [ ] Performance testing integration
- [ ] **Container insights and detailed monitoring**
- [ ] **Custom domain name with Route 53**

---

**Author**: Neeraj  
**Project**: DevOps CI/CD Pipeline  
**Date**: September 2025
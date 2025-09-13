# DevOps CI/CD Pipeline Project

A complete CI/CD pipeline implementation for a Node.js application using Jenkins, Docker, AWS ECS, and CloudWatch monitoring.

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
```

## 📋 Project Overview

This project demonstrates a complete DevOps CI/CD pipeline with:
- **Source Control**: GitHub with branching strategy (main/dev)
- **CI/CD**: Jenkins pipeline with automated builds
- **Containerization**: Docker with multi-stage builds
- **Registry**: DockerHub for image storage
- **Deployment**: AWS ECS (Fargate) for container orchestration
- **Monitoring**: CloudWatch for logs and metrics

## 🚀 Pipeline Flow

### 1. Code Commit
- Developer pushes code to `dev` branch
- GitHub webhook triggers Jenkins pipeline

### 2. Build Stage
- Install Node.js dependencies (`npm install`)
- Run automated tests (`npm test`)
- Validate application structure

### 3. Dockerize Stage
- Build Docker image with application
- Tag image with build number
- Create latest tag for deployment

### 4. Push to Registry
- Authenticate with DockerHub
- Push tagged images to registry
- Images available for deployment

### 5. Deploy Stage
- Update ECS task definition
- Deploy to AWS ECS Fargate
- Zero-downtime deployment

### 6. Monitoring
- CloudWatch logs collection
- CPU/Memory metrics monitoring
- Automated alerts for issues

## 🛠️ Setup Instructions

### Prerequisites
- AWS Account with appropriate permissions
- DockerHub account
- GitHub repository
- EC2 instance for Jenkins

### 1. Infrastructure Setup

```bash
# Clone repository
git clone https://github.com/devilraj98/devops-task.git
cd devops-task

# Setup AWS ECS resources
chmod +x ecs-setup.sh
./ecs-setup.sh

# Setup CloudWatch monitoring
chmod +x setup-monitoring.sh
./setup-monitoring.sh
```

### 2. Jenkins Configuration

1. **Install Jenkins on EC2**
   ```bash
   # Install Java, Jenkins, Docker, Node.js
   # Configure security groups (ports 8080, 3000)
   ```

2. **Install Required Plugins**
   - Docker Pipeline
   - GitHub Integration
   - NodeJS Plugin
   - AWS Credentials Plugin

3. **Configure Credentials**
   - DockerHub credentials (`dockerhub-credentials`)
   - AWS credentials (`aws-credentials`)

4. **Create Pipeline Job**
   - Repository: `https://github.com/devilraj98/devops-task.git`
   - Branch: `*/dev`
   - Pipeline script from SCM

### 3. GitHub Webhook Setup

1. Repository Settings → Webhooks
2. Payload URL: `http://your-jenkins-ip:8080/github-webhook/`
3. Content type: `application/json`
4. Events: Push events

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
├── ecs-setup.sh            # AWS ECS setup script
├── setup-monitoring.sh     # CloudWatch setup script
├── cloudwatch-dashboard.json # Monitoring dashboard
└── README.md               # This documentation
```

## 🔧 Configuration Files

### Jenkinsfile Pipeline Stages
- **Build**: Dependencies installation and testing
- **Dockerize**: Container image creation
- **Push**: Registry upload
- **Deploy**: ECS service update

### ECS Task Definition
- **CPU**: 256 units (0.25 vCPU)
- **Memory**: 512 MB
- **Network**: awsvpc mode
- **Launch Type**: Fargate

## 📊 Monitoring & Logging

### CloudWatch Dashboard
- **Metrics**: CPU utilization, Memory usage
- **Logs**: Application logs with timestamps
- **Alarms**: High CPU usage alerts

### Access Monitoring
- **Dashboard**: [CloudWatch Console](https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#dashboards:name=DevOps-Task-Dashboard)
- **Logs**: [CloudWatch Logs](https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#logsV2:log-groups/log-group/%2Fecs%2Fdevops-task)

## 🌐 Application Access

After successful deployment:
- **Application URL**: Check ECS service public IP
- **Port**: 3000
- **Endpoint**: `http://35.175.102.229:3000/`

## 🔄 Branching Strategy

- **main**: Production-ready code
- **dev**: Development and testing
- **Workflow**: Feature → dev → Pull Request → main

## 🚨 Troubleshooting

### Common Issues
1. **Jenkins Build Fails**: Check Node.js tool configuration
2. **Docker Push Denied**: Verify DockerHub credentials
3. **Docker Push Denied**: Jenkins are not added into Docker Group
4. **ECS Deployment Fails**: Check AWS credentials and permissions
5. **Webhook Not Triggering**: Verify GitHub webhook URL

### Logs Location
- **Jenkins**: Build console output
- **Docker**: Container logs via `docker logs`
- **ECS**: CloudWatch logs `/ecs/devops-task`

## 📈 Best Practices Implemented

- ✅ Automated testing in CI pipeline
- ✅ Multi-stage Docker builds
- ✅ Infrastructure as Code (ECS task definitions)
- ✅ Monitoring and alerting
- ✅ Zero-downtime deployments
- ✅ Proper branching strategy
- ✅ Security best practices (credentials management)

## 🎯 Future Enhancements

- [ ] Terraform for complete Infrastructure as Code
- [ ] Blue-Green deployment strategy
- [ ] Automated rollback on failure
- [ ] Security scanning in pipeline
- [ ] Performance testing integration

---

**Author**: Neeraj  
**Project**: DevOps CI/CD Pipeline  
**Date**: September 2025
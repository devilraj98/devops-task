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

## 🚀 Production-Ready Hosting Roadmap

### 🔒 **Security Implementation**

#### SSL/TLS & Domain
- [ ] **SSL Certificate**: AWS Certificate Manager (ACM) for HTTPS
- [ ] **Custom Domain**: Route 53 + your domain (e.g., myapp.com)
- [ ] **HTTPS Redirect**: Force all HTTP traffic to HTTPS
- [ ] **Security Headers**: HSTS, CSP, X-Frame-Options

#### Network Security
- [ ] **WAF (Web Application Firewall)**: Block malicious traffic
- [ ] **Private Subnets**: Move ECS tasks to private subnets
- [ ] **NAT Gateway**: For outbound internet access from private subnets
- [ ] **VPC Flow Logs**: Monitor network traffic
- [ ] **Security Groups**: Principle of least privilege

#### Application Security
- [ ] **Container Scanning**: Scan Docker images for vulnerabilities
- [ ] **Secrets Management**: AWS Secrets Manager (no hardcoded secrets)
- [ ] **IAM Roles**: Minimal permissions, no root access
- [ ] **Environment Variables**: Secure configuration management

### 🏗️ **High Availability & Scalability**

#### Multi-AZ Deployment
- [ ] **Multiple Availability Zones**: Deploy across 3 AZs
- [ ] **Auto Scaling**: CPU/Memory based scaling (2-10 tasks)
- [ ] **Health Checks**: ALB + ECS health monitoring
- [ ] **Circuit Breaker**: Graceful failure handling

#### Load Balancing
- [x] **Application Load Balancer**: Already implemented ✅
- [ ] **Sticky Sessions**: If needed for your app
- [ ] **Connection Draining**: Graceful task termination

### 📊 **Monitoring & Observability**

#### Logging
- [x] **Centralized Logging**: CloudWatch Logs ✅
- [ ] **Log Retention**: Set appropriate retention (30-90 days)
- [ ] **Structured Logging**: JSON format for better parsing
- [ ] **Error Tracking**: Sentry or similar service

#### Monitoring
- [ ] **CloudWatch Dashboards**: CPU, Memory, Request metrics
- [ ] **Alarms**: High CPU, Memory, Error rates
- [ ] **Uptime Monitoring**: External service (Pingdom, UptimeRobot)
- [ ] **APM**: Application Performance Monitoring

### 🔄 **CI/CD Enhancements**

#### Pipeline Security
- [ ] **Security Scanning**: SAST, DAST, dependency scanning
- [ ] **Code Quality**: SonarQube integration
- [ ] **Approval Gates**: Manual approval for production
- [ ] **Rollback Strategy**: Automated rollback on failure

#### Testing
- [x] **Unit Tests**: Already implemented ✅
- [ ] **Integration Tests**: API endpoint testing
- [ ] **Load Testing**: Performance under stress
- [ ] **Security Tests**: OWASP ZAP scanning

### 💾 **Data & Backup**

#### Database (if needed)
- [ ] **RDS**: Managed database with backups
- [ ] **Multi-AZ**: Database high availability
- [ ] **Read Replicas**: For read scaling
- [ ] **Encryption**: At rest and in transit

#### Backup Strategy
- [x] **ECS Task Definitions**: Version control ✅
- [ ] **Configuration Backup**: Infrastructure as Code
- [ ] **Data Backup**: Automated daily backups

### 🌍 **Performance & CDN**

#### Content Delivery
- [ ] **CloudFront CDN**: Global content distribution
- [ ] **Static Assets**: S3 + CloudFront for images/CSS/JS
- [ ] **Caching Strategy**: Browser and CDN caching
- [ ] **Compression**: Gzip/Brotli compression

### 💰 **Cost Optimization**

#### Resource Management
- [ ] **Right Sizing**: Optimize CPU/Memory allocation
- [ ] **Spot Instances**: For non-critical workloads
- [ ] **Reserved Instances**: For predictable workloads
- [ ] **Cost Monitoring**: AWS Cost Explorer alerts

### 🔧 **Operational Excellence**

#### Documentation
- [ ] **Runbooks**: Incident response procedures
- [ ] **Architecture Diagrams**: Updated documentation
- [ ] **API Documentation**: If applicable
- [ ] **Deployment Guide**: Step-by-step procedures

#### Compliance
- [ ] **GDPR/Privacy**: Data protection compliance
- [ ] **SOC 2**: If handling sensitive data
- [ ] **Audit Logging**: Track all changes
- [ ] **Data Retention**: Compliance with regulations

### 🚨 **Disaster Recovery**

#### Backup & Recovery
- [ ] **Multi-Region**: Cross-region replication
- [ ] **RTO/RPO**: Define recovery objectives
- [ ] **Disaster Recovery Plan**: Tested procedures
- [ ] **Data Replication**: Real-time or scheduled

### 📋 **Implementation Priority**

#### **Phase 1 (Immediate - Security First)**
1. [ ] SSL Certificate + Custom Domain
2. [ ] HTTPS redirect
3. [ ] Security headers
4. [ ] Container vulnerability scanning
5. [ ] Secrets management

#### **Phase 2 (Short-term - High Availability)**
1. [ ] Multi-AZ deployment
2. [ ] Auto scaling
3. [ ] Enhanced monitoring
4. [ ] WAF implementation
5. [ ] Private subnets

#### **Phase 3 (Long-term - Performance & Compliance)**
1. [ ] CDN setup
2. [ ] Multi-region deployment
3. [ ] Advanced security scanning
4. [ ] Compliance implementation
5. [ ] Disaster recovery testing

> **💡 Recommendation**: Start with Phase 1 for a secure, production-ready website. Each phase builds upon the previous one to create an enterprise-grade hosting solution.

## 🎯 Interview Questions for 4-Year AWS DevOps Engineer

### 📋 **Project Overview Questions**

**Q1: Walk me through your CI/CD pipeline architecture**
- GitHub webhook triggers Jenkins pipeline
- 5 stages: Infrastructure Setup, Build, Dockerize, Push, Deploy
- Automated AWS resource provisioning (ECS, ALB, IAM)
- Zero-downtime deployments with Application Load Balancer
- Dynamic account ID detection for multi-account compatibility

**Q2: How did you solve the changing IP address problem?**
- Implemented Application Load Balancer (ALB) for fixed endpoint
- ALB provides permanent DNS name that doesn't change
- Target groups automatically register/deregister ECS tasks
- Health checks ensure traffic only goes to healthy containers

### 🏗️ **AWS Infrastructure Questions**

**Q3: Explain your ECS architecture and why you chose Fargate**
- ECS Fargate for serverless container management
- No EC2 instance management required
- awsvpc networking mode for better security
- Task definitions define CPU/memory allocation (256 CPU, 512 MB)
- Auto-scaling capabilities without infrastructure overhead

**Q4: How do you handle IAM roles and permissions in your pipeline?**
- Created ecsTaskExecutionRole with minimal required permissions
- Dynamic account ID detection using `aws sts get-caller-identity`
- Principle of least privilege for security
- Automated IAM role creation in infrastructure setup
- Separate roles for Jenkins and ECS tasks

**Q5: Describe your Application Load Balancer configuration**
- ALB listens on port 80 (HTTP)
- Target group routes to container port 3000
- Health checks on root path "/"
- Target type "ip" for Fargate compatibility
- Security groups allow inbound traffic on port 80

### 🔧 **DevOps Tools & Practices**

**Q6: How do you ensure your infrastructure scripts are idempotent?**
- Check if resources exist before creating them
- Use conditional logic in bash scripts
- AWS CLI queries to verify resource state
- Error handling with `2>/dev/null` for graceful failures
- Safe to run multiple times without side effects

**Q7: Explain your Docker strategy and multi-stage builds**
- Dockerfile optimized for Node.js applications
- Multi-stage builds to reduce image size
- .dockerignore to exclude unnecessary files
- Image tagging with build numbers for versioning
- DockerHub registry for image storage

**Q8: How do you handle secrets and sensitive data?**
- Jenkins credentials plugin for DockerHub and AWS access
- No hardcoded secrets in code or Dockerfiles
- Environment variables for configuration
- Future: AWS Secrets Manager for production
- Credential rotation and access control

### 📊 **Monitoring & Troubleshooting**

**Q9: What monitoring and logging have you implemented?**
- CloudWatch Logs for centralized logging
- Log group `/ecs/devops-task` for application logs
- Container-level logging with awslogs driver
- Future: CloudWatch dashboards and alarms
- Application and infrastructure metrics

**Q10: How would you troubleshoot a failed deployment?**
- Check Jenkins console output for pipeline failures
- Verify ECS service status and task health
- Check ALB target group health status
- Review CloudWatch logs for application errors
- Validate security group rules and network connectivity
- Use AWS CLI commands for debugging

### 🔄 **CI/CD & Automation**

**Q11: How do you ensure zero-downtime deployments?**
- ALB health checks before routing traffic
- ECS rolling deployments with new task definitions
- `aws ecs wait services-stable` for deployment completion
- Target group draining for graceful shutdowns
- Blue-green deployment strategy for future enhancement

**Q12: Explain your branching strategy and webhook configuration**
- Git flow: feature → dev → main branches
- GitHub webhooks trigger on push to dev branch
- Jenkins pipeline configured for automatic builds
- Pull request workflow for code review
- Environment-specific deployments

### 🛡️ **Security Questions**

**Q13: What security measures have you implemented?**
- Security groups with minimal required ports
- IAM roles with least privilege principle
- VPC networking for container isolation
- No hardcoded credentials in code
- Future: WAF, private subnets, container scanning

**Q14: How would you implement HTTPS and SSL certificates?**
- AWS Certificate Manager (ACM) for SSL certificates
- ALB listener on port 443 with SSL termination
- HTTP to HTTPS redirect rules
- Route 53 for custom domain management
- Security headers implementation

### 🚀 **Scalability & Performance**

**Q15: How would you implement auto-scaling for this application?**
- ECS Service auto-scaling based on CPU/memory metrics
- CloudWatch alarms for scaling triggers
- Target tracking scaling policies
- ALB distributes load across multiple tasks
- Multi-AZ deployment for high availability

**Q16: Describe your disaster recovery strategy**
- Multi-region deployment for DR
- RTO/RPO requirements definition
- Automated backup strategies
- Infrastructure as Code for quick recovery
- Database replication if applicable

### 💰 **Cost Optimization**

**Q17: How do you optimize costs in your AWS infrastructure?**
- Right-sizing ECS tasks (CPU/memory allocation)
- Fargate Spot for non-critical workloads
- Reserved instances for predictable workloads
- CloudWatch cost monitoring and alerts
- Resource cleanup automation

### 🔧 **Advanced Technical Questions**

**Q18: How would you implement blue-green deployments?**
- Two identical environments (blue/green)
- ALB target groups for traffic switching
- Automated testing in green environment
- Instant rollback capability
- Database migration strategies

**Q19: Explain how you would migrate this to Kubernetes**
- EKS cluster setup with worker nodes
- Kubernetes deployments and services
- Ingress controllers for load balancing
- Helm charts for application packaging
- CI/CD pipeline modifications for kubectl

**Q20: How would you implement Infrastructure as Code with Terraform?**
- Terraform modules for reusable components
- State management with S3 backend
- Environment-specific variable files
- Terraform plan/apply in CI/CD pipeline
- Resource tagging and naming conventions

### 🎯 **Scenario-Based Questions**

**Q21: Your application is experiencing high latency. How do you investigate?**
- Check ALB target group response times
- Review ECS task CPU/memory utilization
- Analyze CloudWatch logs for errors
- Implement APM tools for detailed tracing
- Consider CDN for static content delivery

**Q22: How would you handle a security breach in your pipeline?**
- Immediate credential rotation
- Review access logs and audit trails
- Implement additional security scanning
- Update security groups and IAM policies
- Incident response documentation

### 📚 **Key Terms & Technologies to Master**

**AWS Services**: ECS, Fargate, ALB, CloudWatch, IAM, VPC, Route 53, ACM
**DevOps Tools**: Jenkins, Docker, Git, GitHub Webhooks
**Concepts**: CI/CD, Infrastructure as Code, Zero-downtime deployment, Blue-green deployment
**Security**: IAM roles, Security groups, Secrets management, Container scanning
**Monitoring**: CloudWatch Logs, Metrics, Alarms, Dashboards
**Networking**: VPC, Subnets, Security groups, Load balancers, Target groups

> **💡 Pro Tip**: Be ready to draw architecture diagrams and explain the data flow through your pipeline!

---

**Author**: Neeraj  
**Project**: DevOps CI/CD Pipeline  
**Date**: September 2025
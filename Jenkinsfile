pipeline {
    agent any
    
    tools {
        nodejs 'NodeJS-18'
    }
    
    environment {
        DOCKER_IMAGE = 'neeraj98/devops-task'
        DOCKER_TAG = "${BUILD_NUMBER}"
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')
        AWS_CREDENTIALS = credentials('aws-credentials')
        AWS_DEFAULT_REGION = 'us-east-1'
    }
 
    triggers {
        githubPush()
    }
    
    stages {
        stage('Infrastructure Setup') {
            steps {
                echo 'Setting up AWS ECS infrastructure...'
                sh '''
                    # Make script executable
                    chmod +x ecs-setup.sh
                    
                    # Run infrastructure setup (idempotent)
                    ./ecs-setup.sh || echo "Infrastructure already exists or setup completed"
                '''
            }
        }
        
        stage('Build') {
            steps {
                echo 'Installing dependencies...'
                sh 'npm install'
                echo 'Running tests...'
                sh 'npm test --if-present'
            }
        }
        
        stage('Dockerize') {
            steps {
                echo 'Building Docker image...'
                sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
                sh "docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest"
            }
        }
        
        stage('Push to Registry') {
            steps {
                echo 'Pushing to DockerHub...'
                sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
                sh "docker push ${DOCKER_IMAGE}:${DOCKER_TAG}"
                sh "docker push ${DOCKER_IMAGE}:latest"
            }
        }
        
        stage('Deploy') {
            steps {
                echo 'Deploying to AWS ECS...'
                sh '''
                    # Register new task definition with updated image
                    TASK_DEF_ARN=$(aws ecs register-task-definition \
                        --cli-input-json file://task-definition.json \
                        --region us-east-1 \
                        --query 'taskDefinition.taskDefinitionArn' \
                        --output text)
                    
                    # Check if service exists
                    SERVICE_EXISTS=$(aws ecs describe-services \
                        --cluster devops-cluster \
                        --services devops-service \
                        --region us-east-1 \
                        --query 'services[0].status' \
                        --output text 2>/dev/null || echo "None")
                    
                    if [ "$SERVICE_EXISTS" = "None" ] || [ "$SERVICE_EXISTS" = "INACTIVE" ]; then
                        echo "Creating new ECS service..."
                        # Get VPC and subnet info for service creation
                        VPC_ID=$(aws ec2 describe-vpcs --filters "Name=is-default,Values=true" --query "Vpcs[0].VpcId" --output text --region us-east-1)
                        SUBNET_IDS=$(aws ec2 describe-subnets --filters "Name=vpc-id,Values=$VPC_ID" --query "Subnets[0:2].SubnetId" --output text --region us-east-1 | tr '\t' ',')
                        SECURITY_GROUP_ID=$(aws ec2 describe-security-groups --filters "Name=group-name,Values=devops-ecs-sg" --query "SecurityGroups[0].GroupId" --output text --region us-east-1)
                        
                        aws ecs create-service \
                            --cluster devops-cluster \
                            --service-name devops-service \
                            --task-definition $TASK_DEF_ARN \
                            --desired-count 1 \
                            --launch-type FARGATE \
                            --network-configuration "awsvpcConfiguration={subnets=[$SUBNET_IDS],securityGroups=[$SECURITY_GROUP_ID],assignPublicIp=ENABLED}" \
                            --region us-east-1
                    else
                        echo "Updating existing ECS service..."
                        aws ecs update-service \
                            --cluster devops-cluster \
                            --service devops-service \
                            --task-definition $TASK_DEF_ARN \
                            --region us-east-1
                    fi
                    
                    # Wait for deployment to complete
                    aws ecs wait services-stable \
                        --cluster devops-cluster \
                        --services devops-service \
                        --region us-east-1
                '''
            }
        }
    }
    
    post {
        always {
            sh 'docker logout'
            cleanWs()
        }
    }
}
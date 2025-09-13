pipeline {
    agent any
    
    tools {
        nodejs 'NodeJS-18'
    }
    
    environment {
        DOCKER_IMAGE = 'neeraj98/devops-task'
        DOCKER_TAG = "${BUILD_NUMBER}"
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')
    }
    
    triggers {
        githubPush()
    }
    
    stages {
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
                echo 'Deploying application...'
                sh "docker run -d -p 3000:3000 --name devops-app-${BUILD_NUMBER} ${DOCKER_IMAGE}:latest"
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
pipeline {
    agent any
    
    environment {
        DOCKER_USERNAME = 'your-dockerhub-username'  // Replace with your Docker Hub username
        IMAGE_NAME = 'cyber-def25-malware-detector'
        IMAGE_TAG = "${BUILD_NUMBER}"
        DOCKER_CREDENTIALS_ID = 'dockerhub-credentials'  // Jenkins credentials ID
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out code from repository...'
                checkout scm
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    echo 'Building Docker image...'
                    sh """
                        docker build -t ${DOCKER_USERNAME}/${IMAGE_NAME}:${IMAGE_TAG} .
                        docker tag ${DOCKER_USERNAME}/${IMAGE_NAME}:${IMAGE_TAG} ${DOCKER_USERNAME}/${IMAGE_NAME}:latest
                    """
                }
            }
        }
        
        stage('Push to Docker Hub') {
            steps {
                script {
                    echo 'Pushing image to Docker Hub...'
                    withCredentials([usernamePassword(
                        credentialsId: "${DOCKER_CREDENTIALS_ID}",
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )]) {
                        sh """
                            echo \$DOCKER_PASS | docker login -u \$DOCKER_USER --password-stdin
                            docker push ${DOCKER_USERNAME}/${IMAGE_NAME}:${IMAGE_TAG}
                            docker push ${DOCKER_USERNAME}/${IMAGE_NAME}:latest
                            docker logout
                        """
                    }
                }
            }
        }
        
        stage('Run with Docker Compose') {
            steps {
                script {
                    echo 'Running application with Docker Compose...'
                    sh """
                        # Create network_logs directory if it doesn't exist
                        mkdir -p network_logs output
                        
                        # Stop and remove any existing containers
                        docker-compose down || true
                        
                        # Set environment variable for docker-compose
                        export DOCKER_USERNAME=${DOCKER_USERNAME}
                        
                        # Run with docker-compose
                        docker-compose up --abort-on-container-exit
                    """
                }
            }
        }
    }
    
    post {
        always {
            echo 'Cleaning up...'
            sh 'docker-compose down || true'
        }
        success {
            echo 'Pipeline completed successfully!'
            archiveArtifacts artifacts: 'output/alerts.csv', allowEmptyArchive: true
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}

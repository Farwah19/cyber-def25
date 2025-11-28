pipeline {
    agent any
    
    environment {
        IMAGE_NAME = "cyber-def25-malware-detector"
        DOCKER_USERNAME = "zumarr"
    }
    
    stages {
        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                script {
                    sh 'docker build -t $DOCKER_USERNAME/$IMAGE_NAME:$BUILD_NUMBER .'
                    sh 'docker tag $DOCKER_USERNAME/$IMAGE_NAME:$BUILD_NUMBER $DOCKER_USERNAME/$IMAGE_NAME:latest'
                }
            }
        }
        
        stage('Push to Docker Hub') {
            steps {
                echo 'Pushing image to Docker Hub...'
                script {
                    withCredentials([usernamePassword(
                        credentialsId: 'dockerhub-credentials',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )]) {
                        sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                        sh 'docker push $DOCKER_USERNAME/$IMAGE_NAME:$BUILD_NUMBER'
                        sh 'docker push $DOCKER_USERNAME/$IMAGE_NAME:latest'
                        sh 'docker logout'
                    }
                }
            }
        }
        
        stage('Run with Docker Compose') {
            steps {
                echo 'Running malware detection with Docker Compose...'
                script {
                    sh 'mkdir -p network_logs output'
                    sh 'docker-compose down || true'
                    sh 'docker-compose up -d'
                    sh 'sleep 30'
                    sh 'docker-compose ps'
                    sh 'cat output/alerts.csv || echo "Processing..."'
                }
            }
        }
    }
    
    post {
        always {
            echo 'Cleaning up...'
            sh 'docker-compose down || true'
            sh 'docker system prune -af --volumes || true'
        }
        success {
            echo 'Pipeline completed successfully!'
            archiveArtifacts artifacts: 'output/alerts.csv', allowEmptyArchive: true
        }
        failure {
            echo 'Pipeline failed. Check logs.'
        }
    }
}

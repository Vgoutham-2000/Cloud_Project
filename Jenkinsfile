pipeline { 
    environment {
        IMAGE = "vgoutham3007/my_app"
        dockerImage = ''
    }
    agent any 
    stages {
        stage('checkout') {
            steps {
                git branch: 'main',
                url: 'https://github.com/Abinashkhuntia/jenkins_task_revature.git'
            }
        }
        stage('remove the existing container and images') {
            steps {
                script {
                    sh "docker rm demoapp || true"
                    sh "docker rmi ${IMAGE}:lts || true"
                }
            }
        }
        stage('Building the image and pushing to dockerhub') {
            steps {
                echo "building the docker image..."
                withCredentials([usernamePassword(credentialsId: 'b4a8af34-f778-49ef-9c08-02a6ad8901e5', passwordVariable: 'PASS', usernameVariable: 'USER')]) {
                    sh "echo $PASS | docker login -u $USER --password-stdin"
                    sh "docker build -t ${IMAGE}:lts ."
                    sh "docker push ${IMAGE}:lts"
                }
            }
        }
        stage('Running the container') {
            steps {
                echo "run boi run."
                sh "docker pull ${IMAGE}:lts"
                sh "docker run -d -p 80:80 --name demoapp ${IMAGE}:lts"
            }
        }
    } 
}
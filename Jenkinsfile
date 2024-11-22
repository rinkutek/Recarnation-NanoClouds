pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git branch: 'master', url: 'https://github.com/rinkutek/Recarnation-TechTitans.git'
            }
        }
        stage('Install Frontend') {
            steps {
                dir('frontend') {
                    bat 'npm install'
                    bat 'npm run build'
                }
            }
        }
        stage('Install Backend') {
            steps {
                dir('backend') {
                    bat 'pip install -r requirements.txt'
                    bat 'python manage.py test'
                }
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploy step skipped as no SSH server is configured.'
            }
        }
    }
}

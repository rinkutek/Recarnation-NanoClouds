pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                // Clone the repository from GitHub
                git branch: 'master', url: 'https://github.com/rinkutek/Recarnation-TechTitans.git'
            }
        }
        stage('Setup Backend') {
            steps {
                dir('backend') {
                    // Use a virtual environment to install Python dependencies
                    sh '''
                    python -m venv venv
                    source venv/bin/activate
                    pip install -r requirements.txt
                    '''
                }
            }
        }
        stage('Run Backend Tests') {
            steps {
                dir('backend') {
                    // Run Django tests
                    sh '''
                    source venv/bin/activate
                    python manage.py test
                    '''
                }
            }
        }
        stage('Prepare Frontend') {
            steps {
                dir('frontend') {
                    // If static HTML exists, copy it to the deployment location
                    sh '''
                    mkdir -p /var/www/html
                    cp -R * /var/www/html
                    '''
                }
            }
        }
        stage('Run Backend Server') {
            steps {
                dir('backend') {
                    // Start the Django development server
                    sh '''
                    source venv/bin/activate
                    python manage.py migrate
                    nohup python manage.py runserver 0.0.0.0:8000 &
                    '''
                }
            }
        }
    }
    post {
        always {
            echo 'Pipeline execution complete.'
        }
    }
}

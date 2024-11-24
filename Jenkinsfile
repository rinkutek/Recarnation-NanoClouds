pipeline {
    agent any

    environment {
        PYTHON_VERSION = '3.8'
        VENV_NAME = 'venv'
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout code from GitHub
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            steps {
                sh '''
                    # Create and activate virtual environment
                    python${PYTHON_VERSION} -m venv ${VENV_NAME}
                    . ${VENV_NAME}/bin/activate
                    
                    # Upgrade pip
                    pip install --upgrade pip
                    
                    # Install project dependencies
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    . ${VENV_NAME}/bin/activate
                    
                    # Run Django tests
                    python manage.py test
                    
                    # Run any additional test suites
                    # pytest if you're using it
                    # coverage run manage.py test (if using coverage)
                '''
            }
        }

        stage('Static Code Analysis') {
            steps {
                sh '''
                    . ${VENV_NAME}/bin/activate
                    
                    # Run pylint
                    pylint --exit-zero **/*.py
                    
                    # Run flake8
                    flake8 --exit-zero .
                '''
            }
        }

        stage('Collect Static Files') {
            steps {
                sh '''
                    . ${VENV_NAME}/bin/activate
                    
                    # Collect static files
                    python manage.py collectstatic --noinput
                '''
            }
        }

        stage('Database Migrations') {
            steps {
                sh '''
                    . ${VENV_NAME}/bin/activate
                    
                    # Run migrations
                    python manage.py migrate --noinput
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    . ${VENV_NAME}/bin/activate
                    
                    # Add your deployment commands here
                    # This could be deploying to a server, container, or cloud service
                    echo "Deploying application..."
                '''
            }
        }
    }

    post {
        always {
            // Clean up workspace
            cleanWs()
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}

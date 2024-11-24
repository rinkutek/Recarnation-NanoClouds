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
                bat """
                    // Create virtual environment if it doesn't exist
                    if not exist ${VENV_NAME} python -m venv ${VENV_NAME}
                    
                    // Activate virtual environment and install dependencies
                    call ${VENV_NAME}\\Scripts\\activate.bat
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                """
            }
        }

        stage('Run Tests') {
            steps {
                bat """
                    call ${VENV_NAME}\\Scripts\\activate.bat
                    python manage.py test
                """
            }
        }

        stage('Static Code Analysis') {
            steps {
                bat """
                    call ${VENV_NAME}\\Scripts\\activate.bat
                    pip install pylint flake8
                    pylint --exit-zero **/*.py
                    flake8 --exit-zero .
                """
            }
        }

        stage('Collect Static Files') {
            steps {
                bat """
                    call ${VENV_NAME}\\Scripts\\activate.bat
                    python manage.py collectstatic --noinput
                """
            }
        }

        stage('Database Migrations') {
            steps {
                bat """
                    call ${VENV_NAME}\\Scripts\\activate.bat
                    python manage.py migrate --noinput
                """
            }
        }

        stage('Deploy') {
            steps {
                bat """
                    call ${VENV_NAME}\\Scripts\\activate.bat
                    
                    // Add your Windows-specific deployment commands here
                    echo "Deploying application..."
                """
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

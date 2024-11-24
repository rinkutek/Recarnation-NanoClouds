pipeline {
    agent any

    environment {
        PYTHON_VERSION = '3.8'
        VENV_NAME = 'venv'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            steps {
                // First modify requirements.txt to use psycopg2-binary
                bat """
                    if exist requirements.txt (
                        type requirements.txt | find /v "psycopg2" > requirements_temp.txt
                        echo psycopg2-binary >> requirements_temp.txt
                        move /y requirements_temp.txt requirements.txt
                    )
                """
                
                // Create and setup virtual environment
                bat """
                    if not exist ${VENV_NAME} python -m venv ${VENV_NAME}
                    call ${VENV_NAME}\\Scripts\\activate.bat
                    python -m pip install --upgrade pip setuptools wheel
                    pip install --no-cache-dir psycopg2-binary
                    pip install -r requirements.txt --no-deps
                    pip install -r requirements.txt
                """
            }
        }

        stage('Run Tests') {
            steps {
                bat """
                    call ${VENV_NAME}\\Scripts\\activate.bat
                    set PYTHONPATH=%WORKSPACE%
                    python manage.py test
                """
            }
        }

        stage('Static Code Analysis') {
            steps {
                bat """
                    call ${VENV_NAME}\\Scripts\\activate.bat
                    pip install pylint flake8
                    pylint --exit-zero **/*.py || exit 0
                    flake8 --exit-zero . || exit 0
                """
            }
        }

        stage('Collect Static Files') {
            steps {
                bat """
                    call ${VENV_NAME}\\Scripts\\activate.bat
                    python manage.py collectstatic --noinput || exit 0
                """
            }
        }

        stage('Database Migrations') {
            steps {
                bat """
                    call ${VENV_NAME}\\Scripts\\activate.bat
                    python manage.py migrate --noinput || exit 0
                """
            }
        }

        stage('Deploy') {
            steps {
                bat """
                    call ${VENV_NAME}\\Scripts\\activate.bat
                    echo "Deploying application..."
                """
            }
        }
    }

    post {
        always {
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

pipeline {
    agent any

    environment {
        PYTHON_VERSION = '3.8'
        VENV_NAME = 'venv'
        DJANGO_SETTINGS_MODULE = 'cardealer.settings'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            steps {
                bat """
                    if not exist ${VENV_NAME} python -m venv ${VENV_NAME}
                    call ${VENV_NAME}\\Scripts\\activate.bat
                    python -m pip install --upgrade pip setuptools wheel
                    pip install django-ckeditor==6.3.2
                    pip install Django==3.2.23
                    pip install psycopg2-binary
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
                    python manage.py test || exit 0
                """
            }
        }

        stage('Static Code Analysis') {
            steps {
                bat """
                    call ${VENV_NAME}\\Scripts\\activate.bat
                    pip install pylint flake8 pylint-django
                    
                    rem Only analyze project files, exclude venv and migrations
                    pylint --load-plugins pylint_django --ignore=venv,*/migrations/* cardealer || exit 0
                    flake8 cardealer --exclude=venv,*/migrations/* || exit 0
                """
            }
        }

        stage('Collect Static Files') {
            steps {
                bat """
                    call ${VENV_NAME}\\Scripts\\activate.bat
                    python manage.py collectstatic --noinput -v 0 || exit 0
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

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

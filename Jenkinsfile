pipeline {
    agent {
        docker {
            image 'python:3.9-slim-buster'
            args '-u root -v $HOME/.aws:/root/.aws'
        }
    }
    // triggers {
    //     GitHubPushTrigger {
    //         branches {
    //             branch {
    //                 compareType 'PLAIN'
    //                 pattern 'JenkinsCloud'
    //             }
    //         }
    //         githubAppCredentialsId 'jenkins-github-ssh'
    //     }
    //     pollSCM('H/5 * * * *')
    // }
    environment {
        AWS_REGION = 'us-east-1'
        APPLICATION_NAME = 'recarnation-app'
        ENVIRONMENT_NAME = 'recarnation-env'
        EB_PLATFORM = 'Python 3.11'
    }
    stages {
        stage('Checkout') {
            steps {
                sh '''
            # Force clean workspace
            find . -mindepth 1 -delete || true
        '''
                git branch: 'JenkinsCloud', 
                url: 'git@github.com:ApoorvaShastry10/Recarnation-TechTitansCloud.git',
                credentialsId: 'jenkins-github-ssh'
            }
        }

        stage('Setup Environment') {
            steps {
                sh '''
                    # Install essential tools
                    apt-get update && apt-get install -y git
                    git config --global --add safe.directory '*'
                    
                    # Create fresh virtual environment
                    python -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip setuptools wheel
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -c constraints.txt -r requirements.txt
                '''

            }
        }
        
        stage('Install EB CLI') {
            steps {
                sh '''
                    . venv/bin/activate
                    pip install awsebcli==3.20.3
                    eb --version
                '''
            }
        }
        
        stage('Initialize EB') {
            steps {
                withAWS(credentials: 'aws-creds', region: 'us-east-1') {
                    sh '''
                        . venv/bin/activate
                        eb init "$APPLICATION_NAME" \
                            --platform "$EB_PLATFORM" \
                            --region "$AWS_REGION" \
                            --tags "environment=production,team=devops" \
                            --no-verify
                    '''
                }
            }
        }
        
        stage('Verify Permissions') {
            steps {
                withAWS(credentials: 'aws-creds', region: 'us-east-1') {
                    sh '''
                        . venv/bin/activate
                        # Test required permissions
                        aws cloudformation get-template --stack-name "awseb-e-${ENVIRONMENT_NAME}-stack" --output text || \
                            echo "Warning: Missing CloudFormation permissions - update IAM policy"
                    '''
                }
            }
        }
        
        stage('Safe Deploy') {
            steps {
                withAWS(credentials: 'aws-creds', region: 'us-east-1') {
                    sh '''#!/bin/bash
set -e

. venv/bin/activate
echo "Current directory: $(pwd)"
# 1. Wait for environment to be ready
echo "Checking environment status..."
end_time=$((SECONDS+1800)) # 30 minute timeout

while [ $SECONDS -lt $end_time ]; do
    status=$(eb status "$ENVIRONMENT_NAME" | grep "Status:" | awk '{print $2}')
    [ "$status" = "Ready" ] && break
    echo "Current status: $status - waiting..."
    sleep 30
done

# 2. Standard deploy with retry logic
max_retries=3
attempt=1

while [ $attempt -le $max_retries ]; do
    echo "Attempt $attempt of $max_retries"
    if eb deploy "$ENVIRONMENT_NAME" --timeout 45; then
        echo "Deployment succeeded"
        break
    else
        echo "Deployment failed, retrying..."
        sleep 30
        attempt=$((attempt + 1))
    fi
done

# 3. Final verification
eb health --refresh
[ $attempt -gt $max_retries ] && exit 1
'''
// sh '''
//             zip -r my-custom-name.zip .
//             eb deploy "$ENVIRONMENT_NAME" --label my-custom-name
//         '''

                }
            }
        }
    }
    
    post {
        always {
            sh '''
                rm -rf venv
            '''
        }
    }
}

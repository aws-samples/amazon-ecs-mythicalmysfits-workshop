#! /bin/bash

set -eu

# Install Go
sudo yum install go -y

# Configure Docker
mkdir -p /home/participant/.docker
cat << EOF > /home/participant/.docker/config.json
{
	"credsStore": "ecr-login"
}
EOF
chown -R participant. /home/participant/.docker

# Build credential helper
rm -rf amazon-ecr-credential-helper
git clone https://github.com/awslabs/amazon-ecr-credential-helper.git
cd amazon-ecr-credential-helper
make
sudo cp bin/local/docker-credential-ecr-login /usr/local/bin/

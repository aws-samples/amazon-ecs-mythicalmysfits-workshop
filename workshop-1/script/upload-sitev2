#! /bin/bash

set -eu

# Use AWS_REGION from environment
REGION=${AWS_REGION}

# Use absolute paths for all files
if [[ $# -eq 1 ]]; then
  BUCKET_NAME="$1"
else
  BUCKET_NAME=$(jq < /environment/workshop-1/cfn-output.json -r '.SiteBucket')
fi

if [[ -z $BUCKET_NAME ]]; then
  echo "Unable to determine S3 bucket to use. Ensure that it is returned as an output from CloudFormation or passed as the first argument to the script."
  exit 1
fi

API_ENDPOINT=$(jq < /environment/workshop-1/cfn-output.json -r '.LoadBalancerDNS')

echo "Using bucket: $BUCKET_NAME"
echo "API endpoint: $API_ENDPOINT"
echo "Region: $REGION"

# Create temp directory with proper permissions
TEMP_DIR=$(mktemp -d)
chmod 755 $TEMP_DIR

echo "Copying web files to temp directory: $TEMP_DIR"
cp -R /environment/workshop-1/web/. $TEMP_DIR/

# Use sed directly
echo "Updating API endpoint in HTML files"
sed -i "s|REPLACE_ME_API_ENDPOINT|http://$API_ENDPOINT|g" $TEMP_DIR/index.html
sed -i "s|REPLACE_ME_API_ENDPOINT|http://$API_ENDPOINT|g" $TEMP_DIR/register.html
sed -i "s|REPLACE_ME_API_ENDPOINT|http://$API_ENDPOINT|g" $TEMP_DIR/confirm.html

echo "Updating web endpoint in HTML files"
sed -i "s|REPLACE_ME_WEB_ENDPOINT|$BUCKET_NAME.s3.amazonaws.com|g" $TEMP_DIR/index.html
sed -i "s|REPLACE_ME_WEB_ENDPOINT|$BUCKET_NAME.s3.amazonaws.com|g" $TEMP_DIR/register.html
sed -i "s|REPLACE_ME_WEB_ENDPOINT|$BUCKET_NAME.s3.amazonaws.com|g" $TEMP_DIR/confirm.html

echo "Syncing files to S3 bucket: $BUCKET_NAME"
aws s3 sync $TEMP_DIR s3://$BUCKET_NAME

# Upload images to the correct path
echo "Uploading images to web/images path"
aws s3 cp /environment/workshop-1/web/images s3://$BUCKET_NAME/web/images --recursive

echo "Upload complete. Website URL: http://$BUCKET_NAME.s3-website-$REGION.amazonaws.com"

# Script to create a base layer for AWS Lambda functions
# This layer will contain the basic dependencies that are required for most of the Lambda functions
# The layer will be created with the name base-dependencies-layer   
# The layer will be compatible with Python 3.8, 3.9, 3.10, 3.11, and 3.12
# The layer will contain the following dependencies:
# 1. requests==2.31.0
# 2. urllib3==1.26.15
# 3. pytz

# Open AWS CloudShell
# Step 1: Clean up any previous attempt
rm -rf base_layer
mkdir base_layer
cd base_layer
mkdir python

# Step 2: Install specific versions to avoid conflicts
pip install requests==2.31.0 urllib3==1.26.15 -t python/
pip install pytz -t python/

# Step 3: Zip the directory
zip -r base_layer.zip python

# Step 4: Publish the layer
aws lambda publish-layer-version --layer-name base-dependencies-layer --zip-file fileb://base_layer.zip --compatible-runtimes python3.8 python3.9 python3.10 python3.11 python3.12

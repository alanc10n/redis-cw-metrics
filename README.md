# redis-cw-metrics
Python script for publishing Redis metrics to AWS Cloudwatch

## Usage

AWS credentials are required to interact with the Cloudwatch service; in the case of services, these are generally made 
available by the EC2 Instance Metadata service when you specify an IAM role. Depending on your application, though, one 
of a number of other configuration methods may be appropriate. See http://boto3.readthedocs.io/en/latest/guide/configuration.html 
for details.

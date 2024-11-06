This will serve as the basis to build AMIs for Autocon labs
This script should be dropped into the advanced->userdata section of the AMI in order to automatically install the needed software before snapshotting the AMI. 

IF you would like the use AWS cli to do this the following commandline can be used:
aws ec2 run-instances \
    --image-id ami-0ea3c35c5c3284d82 \
    --instance-type t3.2xlarge \
    --key-name <key-pair-name> \
    --security-group-ids <security-group-id> \
    --subnet-id <subnet-id> \
    --user-data file://userdata.sh \
    --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=<your-instance-name>}]'




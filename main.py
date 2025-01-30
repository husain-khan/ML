import boto3

# Replace with your AWS credentials if not using IAM role
aws_access_key = "YOUR_ACCESS_KEY"
aws_secret_key = "YOUR_SECRET_KEY"
region = "us-east-1"

# Initialize session
session = boto3.Session(
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key,
    region_name=region
)

ec2 = session.resource("ec2")
client = session.client("ec2")

# 1️⃣ Create a Security Group
security_group = client.create_security_group(
    Description="Automated security group for EC2",
    GroupName="AutoSecurityGroup",
    VpcId="YOUR_VPC_ID"  # Replace with your VPC ID
)

security_group_id = security_group["GroupId"]
print(f"✅ Security Group Created: {security_group_id}")

# 2️⃣ Add Inbound Rules (Allow SSH & HTTP)
client.authorize_security_group_ingress(
    GroupId=security_group_id,
    IpPermissions=[
        {
            "IpProtocol": "tcp",
            "FromPort": 22,
            "ToPort": 22,
            "IpRanges": [{"CidrIp": "0.0.0.0/0"}]  # Allows SSH from anywhere
        },
        {
            "IpProtocol": "tcp",
            "FromPort": 80,
            "ToPort": 80,
            "IpRanges": [{"CidrIp": "0.0.0.0/0"}]  # Allows HTTP access
        }
    ]
)
print("✅ Security Group Rules Configured")

# 3️⃣ Launch an EC2 Instance
instance = ec2.create_instances(
    ImageId="ami-0c55b159cbfafe1f0",  # Replace with a valid AMI ID
    InstanceType="t2.micro",
    MinCount=1,
    MaxCount=1,
    KeyName="your-key",  # Replace with your Key Pair name
    SecurityGroupIds=[security_group_id],
    TagSpecifications=[{"ResourceType": "instance", "Tags": [{"Key": "Name", "Value": "AutoInstance"}]}],
    NetworkInterfaces=[{"AssociatePublicIpAddress": True, "DeviceIndex": 0, "SubnetId": "YOUR_SUBNET_ID"}]
)

instance_id = instance[0].id
print(f"🚀 EC2 Instance Created: {instance_id}")

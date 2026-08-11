#!/bin/bash
# ==============================================================================
# Script Name: user_data.sh
# Description: Launch-time user data bootstrap script for newly-instantiated EC2
#              instances inside the Auto Scaling Group (ASG). Handles standard
#              package updates, installs/starts Apache HTTP Server, resolves IMDSv2
#              instance identifiers (such as Instance ID and Availability Zone),
#              and compiles a structured index.html landing page.
# Usage:        Automatically executed by EC2 launch template bootstrap mechanism.
# Author:       Harisfazillah Jamel (LinuxMalaysia)
# ==============================================================================

# Update system-wide packages and install Apache HTTP Server
dnf update -y
dnf install -y httpd
systemctl start httpd
systemctl enable httpd

# Retrieve metadata via IMDSv2 (using temporary session tokens for high security)
TOKEN=$(curl -s -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")
INSTANCE_ID=$(curl -s -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/instance-id)
AZ=$(curl -s -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/placement/availability-zone)

# Compile the index landing page with local variables
echo "<html>
<head>
    <title>AWS 3-Tier Demo</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f4f4f9; color: #333; }
        .card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); max-width: 600px; margin: auto; }
        h1 { color: #0066cc; }
        .footer { margin-top: 20px; font-size: 0.8em; color: #777; }
    </style>
</head>
<body>
    <div class='card'>
        <h1>Welcome to your AWS 3-Tier Application!</h1>
        <p>This is the application/web layer, running inside a secure, private subnet auto-scaled with an ASG and load balanced by an ALB protected by AWS WAFv2.</p>
        <hr/>
        <p><strong>Instance Metadata:</strong></p>
        <ul>
            <li><strong>Instance ID:</strong> $INSTANCE_ID</li>
            <li><strong>Availability Zone:</strong> $AZ</li>
        </ul>
        <div class='footer'>Deploy managed with OpenTofu.</div>
    </div>
</body>
</html>" > /var/www/html/index.html

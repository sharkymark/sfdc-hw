# Define the argument before its first use
FROM python:3.13-slim

# get utilities in the container
RUN apt-get update && apt-get install -y procps ssh git net-tools htop

# Install pip dependencies
RUN pip install --no-cache-dir --upgrade pip && pip install simple_salesforce


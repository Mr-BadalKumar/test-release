# Use a Python base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the code files to the working directory
COPY . /app


# Set environment variables
ENV host_url="http://20.106.135.93:30793"
ENV argocd_token='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6IkFQSS1UT0tFTjphZG1pbiIsImlzcyI6ImFwaVRva2VuSXNzdWVyIn0.N5wVfiLTTTX0uY9gRd11e33A5g8Bp-Ac3coe_sKdp7Q'

# Install additional dependencies
RUN apt-get update && apt-get install -y \
    git 

# Install YAML package
RUN pip install pyyaml

# Install requests package
RUN pip install requests

# Install any other necessary packages

# Run the code
CMD python dag-release.py


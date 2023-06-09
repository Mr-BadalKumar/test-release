# Use a Python base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the code files to the working directory
COPY dag-release.py  .


# Set environment variables
# Install additional dependencies
RUN apt-get update && apt-get install -y 


RUN pip install  pyyaml


# Install requests package
RUN pip install requests

# Install any other necessary packages

# Run the code
CMD [ "python", "dag-release.py" ]




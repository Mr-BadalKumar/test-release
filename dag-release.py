import json
import requests
import yaml
import os
import subprocess
import datetime

host_url="http://20.106.135.93:30793"
argocd_token='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6IkFQSS1UT0tFTjphZG1pbiIsImlzcyI6ImFwaVRva2VuSXNzdWVyIn0.N5wVfiLTTTX0uY9gRd11e33A5g8Bp-Ac3coe_sKdp7Q'


def find_artifact_id(task_name):
    url = "https://raw.githubusercontent.com/Mr-BadalKumar/test/main/values.yaml"
    response = requests.get(url)
    if response.status_code == 200:
        data = yaml.safe_load(response.content)
        #print(data['component']['casbin']['casbin_ci_artifact_id'])

        CIARTIFACTID= str(data['component'][task_name]['artifact_id'])
        print("ArtifactId Is-: ",CIARTIFACTID)
        return CIARTIFACTID
    else:
        print("Error: Failed to fetch data from URL.")
        print("can not get the artifact id exiting")
        exit

# Read input data from a JSON file
# with open('input.json') as f:
env_var = os.getenv('json_data')
input_data = json.load(env_var)

print(type(input_data))

# Create workflow YAML
workflow_yaml = f"""\
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  name: dag-test
  namespace: argo
spec:
  entrypoint: start
  templates:
    - name: start
      dag:
        tasks:
"""

# Create task YAML for each node in input data
tasks_yaml = ""
for node in input_data:
    task_name = node['name']
    dependencies = node.get('dependencies', [])
    dependencies_yaml = '[' + ', '.join(f"'{d}'" for d in dependencies) + ']'
    task_yaml = f"""\
          - name: {task_name}
            template: {task_name}
            dependencies: {dependencies_yaml}
"""
    if 'having_release' in node and node['having_release'] == "true":
     tasks_yaml += task_yaml

workflow_yaml += tasks_yaml

# Create template YAML for each node in input data
templates_yaml = ""
for node in input_data:
    task_name = node['name']
    env_field = node.get('env_field')
    template_yaml = f"""\
    - name: {task_name}
      container:
        image: badal773/release:02\n"""
    template_yaml += "        env:\n"
    for key, value in env_field.items():
        template_yaml += f"          - name: {key}\n"
        template_yaml += f"""            value: "{value}"\n"""
    artifactId=find_artifact_id(task_name)
    template_yaml += f"          - name: {'CI_ARTIFACT_ID'}\n"
    template_yaml += f"""            value: "{artifactId}"\n"""
    if 'having_release' in node and node['having_release'] == "true":
      templates_yaml += template_yaml

workflow_yaml += templates_yaml



f = open("output.yaml", "w")
f.write(workflow_yaml)
f.close()

# Define repository information
repo_owner = "Mr-BadalKumar"
repo_name = "test-release"
release_version = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")



# # Create a dictionary representing the YAML data
# yaml_data = {
#     "repository": {
#         "owner": repo_owner,
#         "name": repo_name
#     },
#     "release": {
#         "version": release_version
#     }
# }

# Define the filename for the YAML file
yaml_filename = f"{release_version}-release.yaml"

print(workflow_yaml)

# Write the YAML data to the file
with open(yaml_filename, "w") as yaml_file:
    yaml.dump(workflow_yaml, yaml_file)

subprocess.run(["git", "init"])
# Add the YAML file to the Git repository
subprocess.run(["git", "add", yaml_filename])

# Commit the changes
subprocess.run(["git", "commit", "-m", "Add release YAML file"])

subprocess.run(["git", "remote", "add" ,"origin", "https://github.com/Mr-BadalKumar/test-release"])

# Create a Git tag for the release version
tag_name = f"release/{release_version}"
subprocess.run(["git", "tag", tag_name])

# Push the changes and tag to the remote repository
subprocess.run(["git", "push"])
subprocess.run(["git", "push", "--tags"])

import os
import json
import requests

from Factories.Copilot.Services.service_name.Overrides.CfnPatches.factory import CfnPatchesFactory
from Factories.Copilot.Services.service_name.Manifest.factory import ManifestFactory as ServiceManifestFactory
from Factories.Copilot.Environments.environment_name.Manifest.factory import \
    ManifestFactory as EnvironmentManifestFactory
from Factories.Copilot.Workspace.factory import WorkspaceFactory

app_id = os.getenv('NX1_APP_ID', None)
api_url = os.getenv('NX1_API_URL', 'http://localhost:8080/api')
api_token = os.getenv('NX1_API_TOKEN', None)
test_file = os.getenv('NX1_TEST_FILE', None)
env_id = os.getenv('NX1_ENV_ID', None)
data = None

workspace_path = os.getenv('OUTPUT_PATH', '/github/workspace/')

def get_data():
    if not test_file:
        return fetch_data()

    with open(test_file) as json_file:
        return json.load(json_file)


def fetch_data():
    url = api_url + '/apps/' + app_id + '/copilot'
    headers = {'Authorization': 'Bearer ' + api_token}

    response = requests.get(url=url, headers=headers)

    if response.status_code != 200:
        print(f'# Error: NX1 request failed with status code {response.status_code}.')
        exit(1)

    return response.json()

def find_repo_features():
    features = []
    if os.path.isfile(workspace_path + '.nx1-feature-nixpacks'):
        features.append('nixpacks')

    return features

def build_copilot_content():
    repo_features = find_repo_features()

    for environment in data['environments']:
        context = {'environment': environment, 'app': data, 'repo_features': repo_features}
        EnvironmentManifestFactory(environment_name=environment['details']['account_name'], context=context).build()

    for service in data['services']:
        context = {'service': service, 'app': data, 'repo_features': repo_features}
        ServiceManifestFactory(service_name=service['name'], context=context).build()
        CfnPatchesFactory(service_name=service['name'], context=context).build()

    WorkspaceFactory(context={'app_name': data['name']}).build()


def build_service_role_arn(environment_name):
    service_environment = data['services'][0]['environments'][environment_name]

    if not service_environment['service_resources']['service_roles']:
        print('# error: no service role found for environment ' + environment_name)
        exit(1)

    return service_environment['service_resources']['service_roles'][0]['arn']


def write_env_vars():
    if not env_id:
        print('# skipping export env vars since ENV_ID is not specified')
        return

    for environment in data['environments']:
        if environment['details']['uuid'] == env_id:
            github_env_file = os.getenv('GITHUB_ENV')

            if os.getenv('OUTPUT_PATH'):
                github_env_file = os.getenv('OUTPUT_PATH') + 'GITHUB_ENV'

            env_vars = [
                '\nAWS_ACCOUNT_ID=' + environment['details']['aws_account_id'],
                '\nAWS_DEFAULT_REGION=' + environment['details']['aws_region'],
                '\nNX1_ENV=' + environment['details']['account_name'],
                '\nNX1_SERVICE_ROLE_ARN=' + build_service_role_arn(environment['details']['account_name']),
            ]

            for service in data['services']:
                formatted_service_name = service['name'].upper().replace('-', '_')
                env_vars += [
                    '\nNX1_TYPE_' + formatted_service_name + '=' + service['type'],
                ]

            with open(github_env_file, 'a') as file:
                file.writelines(env_vars)

def _validate_inputs():
    if not app_id:
        print('# error: app_id is not specified')
        exit(1)

    if not api_url:
        print('# error: api_url is not specified')
        exit(1)

    if not api_token:
        print('# error: api_token is not specified')
        exit(1)

if __name__ == "__main__":
    _validate_inputs()
    data = get_data()
    build_copilot_content()
    write_env_vars()

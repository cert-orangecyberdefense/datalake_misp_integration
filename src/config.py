import os

incorrect_config_message = 'Config seems incorrect, please check again your env variables'

OCD_DTL_API_ENV = os.getenv('OCD_DTL_API_ENV', 'prod')
assert OCD_DTL_API_ENV in ('prod', 'preprod'), incorrect_config_message

# Max result to push into the misp per query
OCD_DTL_MISP_MAX_RESULT = int(os.getenv('OCD_DTL_MISP_MAX_RESULT', 1000))
assert 0 < OCD_DTL_MISP_MAX_RESULT <= 5000, incorrect_config_message

OCD_DTL_MISP_HOST = os.getenv('OCD_DTL_MISP_HOST', 'http://localhost/')
OCD_DTL_MISP_API_KEY = os.getenv('OCD_DTL_MISP_API_KEY')
assert OCD_DTL_MISP_API_KEY, incorrect_config_message

OCD_DTL_MISP_USE_SSL = os.getenv('OCD_DTL_MISP_USE_SSL', 'True').lower() in ['true', '1']
OCD_DTL_QUERY_CONFIG_PATH = os.getenv('OCD_DTL_QUERY_CONFIG_PATH', 'queries.json')

OCD_DTL_MISP_WORKER = int(os.getenv('OCD_DTL_MISP_WORKER', 4))
assert 0 < OCD_DTL_MISP_WORKER, incorrect_config_message


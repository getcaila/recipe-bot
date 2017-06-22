"""
This module contains the functionality needed to query the Yummly API.
"""

import requests
import os
from collections import OrderedDict

""" --- Constants ---"""
HEADERS = OrderedDict({
	'X-Yummly-App-ID': os.environ["AWS_YUMMLY_APP_ID"],
	'X-Yummly-App-Key': os.environ['AWS_YUMMLY_APP_KEY'],
})

OPTIONAL_PARAMETERS = ['allergy', 'time', 'excluded_ingredient']

YUMMLY_PARAM_MAPPING = {
	'allergy': 'allowedAllergy[]',
	'time': 'maxTotalTimeInSeconds',
	'excluded_ingredient': 'excludedIngredient[]',
}

"""
Method to add optional parameters to payload of parameters for search
"""
def add_optional_parameters(params_dict, additional_params):
	for option in OPTIONAL_PARAMETERS:
		if option in additional_params:
			api_param_name = YUMMLY_PARAM_MAPPING[option]
			params_dict[api_param_name] = additional_params[option]
	return params_dict

"""
Method to create payload of parameters for search
"""
def create_payload(search_term, **options):
	payload = {'q': search_term,
			   'maxResult' : '1',
	}
	if options:
		payload = add_optional_parameters(payload, options)
	return payload

"""
Method to query Yummly API for recipe based on received parameters
"""
def get_search_results(search_term, **options):
	payload = create_payload(search_term, **options)
	r = requests.get('http://api.yummly.com/v1/api/recipes', headers=HEADERS, params=payload)
	r.connection.close()
	return r
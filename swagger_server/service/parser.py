import codecs
import re
import yaml
import json
import six
import sys
import jinja2
import hashlib

from openapi_spec_validator import validate_v2_spec
from openapi_spec_validator import validate_v3_spec
from swagger_parser import SwaggerParser


class Parser(SwaggerParser):
    _HTTP_VERBS = set(['get', 'put', 'post', 'delete', 'options', 'head', 'patch', 'update'])

    def __init__(self, swagger_path=None, swagger_dict=None, swagger_yaml=None, use_example=True):
        """Run parsing from either a file or a dict.

        Args:
            swagger_path: path of the swagger file.
            swagger_dict: swagger dict.
            use_example: Define if we use the example from the YAML when we
                         build definitions example (False value can be useful
                         when making test. Problem can happen if set to True, eg
                         POST {'id': 'example'}, GET /string => 404).

        Raises:
            - ValueError: if no swagger_path or swagger_dict is specified.
                          Or if the given swagger is not valid.
        """
        try:
            if swagger_path is not None:
                # Open yaml file
                arguments = {}
                with codecs.open(swagger_path, 'r', 'utf-8') as swagger_yaml:
                    swagger_template = swagger_yaml.read()
                    swagger_string = jinja2.Template(swagger_template).render(**arguments)
                    self.specification = yaml.safe_load(swagger_string)
            elif swagger_yaml is not None:
                json_ = yaml.safe_load(swagger_yaml)
                json_string = json.dumps(json_)
                self.specification = json.loads(json_string)
            elif swagger_dict is not None:
                self.specification = swagger_dict
            else:
                raise ValueError('You must specify a swagger_path or dict')

            # Validate
            api_version = self.specification['swagger'] if "swagger" in self.specification \
                else self.specification['openapi']
            if '2.0' <= api_version < '3.0':
                validate_v2_spec(self.specification)
            else:
                validate_v3_spec(self.specification)

        except Exception as e:
            six.reraise(
                ValueError,
                ValueError('{0} is not a valid file: {1}'.format(swagger_path, e)),
                sys.exc_info()[2])

        # Run parsing
        self.api_version = self.specification['swagger'] if "swagger" in self.specification \
            else self.specification['openapi']
        self.base_path = "http://" + self.specification.get('host') + self.specification.get('basePath') \
            if '2.0' <= self.api_version < '3.0' \
            else self.specification.get('servers')[0].get('url')
        self.use_example = use_example
        self.info = {}
        self.definitions_example = {}
        self.build_definitions_example()
        self.paths = {}
        self.operation = {}
        self.generated_operation = {}
        self.get_paths_data()

    def get_api_version(self):
        return 2 if '2.0' <= self.api_version < '3.0' else 3

    def build_info(self):
        if "info" in self.specification:
            self.info = {}
            if "title" in self.specification['info']:
                self.info['title'] = self.specification['info']['title']
            if "version" in self.specification['info']:
                self.info['version'] = self.specification['info']['version']
            if "description" in self.specification['info']:
                self.info['description'] = self.specification['info']['description']

    def build_definitions_example(self):
        """Parse all definitions in the swagger specification."""

        for def_name, def_spec in (
        self.specification.get('definitions', {}) if self.get_api_version() == 2 else self.specification.get(
                'components').get('schemas')).items():
            self.build_one_definition_example(def_name)

    def build_one_definition_example(self, def_name):
        """Build the example for the given definition.

        Args:
            def_name: Name of the definition.

        Returns:
            True if the example has been created, False if an error occured.
        """
        api = self.get_api_version()
        definitions = self.specification['definitions'] if api == 2 else self.specification['components']['schemas']

        if def_name in self.definitions_example.keys():  # Already processed
            return True
        elif def_name not in definitions.keys():  # Def does not exist
            return False

        self.definitions_example[def_name] = {}
        def_spec = definitions[def_name]

        if def_spec.get('type') == 'array' and 'items' in def_spec:
            item = self.get_example_from_prop_spec(def_spec['items'])
            self.definitions_example[def_name] = [item]
            return True

        if 'properties' not in def_spec:
            self.definitions_example[def_name] = self.get_example_from_prop_spec(def_spec)
            return True

        # Get properties example value
        for prop_name, prop_spec in def_spec['properties'].items():
            example = self.get_example_from_prop_spec(prop_spec)
            if example is None:
                return False
            self.definitions_example[def_name][prop_name] = example

        return True

    def get_definition_name_from_ref(self, ref):
        """Get the definition name of the given $ref value(Swagger value).

        Args:
            ref: ref value (ex: "#/definitions/CustomDefinition")

        Returns:
            The definition name corresponding to the ref.
        """
        api = self.get_api_version()
        path = '#/definitions/(.*)' if api == 2 else '#/components/schemas/(.*)'
        p = re.compile(path)
        definition_name = re.sub(p, r'\1', ref)
        return definition_name

    def get_paths_data(self):
        """Get data for each paths in the swagger specification.

        Get also the list of operationId.
        """
        for path, path_spec in self.specification['paths'].items():
            path = u'{0}{1}'.format(self.base_path, path)
            self.paths[path] = {}

            # Add path-level parameters
            default_parameters = {}
            if 'parameters' in path_spec:
                self._add_parameters(default_parameters, path_spec['parameters'])

            for http_method in path_spec.keys():
                if http_method not in self._HTTP_VERBS:
                    continue

                self.paths[path][http_method] = {}

                # Add to operation list
                action = path_spec[http_method]
                tag = action['tags'][0] if 'tags' in action.keys() and action['tags'] else None
                if 'operationId' in action.keys():
                    self.operation[action['operationId']] = (path, http_method, tag)
                else:
                    # Note: the encoding chosen below isn't very important in this
                    #       case; what matters is a byte string that is unique.
                    #       URL paths and http methods should encode to UTF-8 safely.
                    h = hashlib.sha256()
                    h.update(("{0}|{1}".format(http_method, path)).encode('utf-8'))
                    self.generated_operation[h.hexdigest()] = (path, http_method, tag)

                # Get parameters
                self.paths[path][http_method]['parameters'] = default_parameters.copy()
                if 'parameters' in action.keys():
                    self._add_parameters(self.paths[path][http_method]['parameters'], action['parameters'])

                # Get responses
                # self.paths[path][http_method]['responses'] = action['responses']

                # Get mime types for this action
                if 'consumes' in action.keys():
                    self.paths[path][http_method]['consumes'] = action['consumes']

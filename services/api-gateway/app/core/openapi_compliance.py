"""
OpenAPI Compliance Module

Ensures API endpoints match their OpenAPI specification.
Provides utilities for validating requests/responses against the spec.
"""

from typing import Dict, Any, Optional, List
from fastapi import Request, Response
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel
import yaml
import json
from pathlib import Path


class OpenAPICompliance:
    """Validates API compliance with OpenAPI specification"""
    
    def __init__(self, spec_path: str = "/workspace/openapi.yaml"):
        """Initialize with OpenAPI specification"""
        self.spec_path = Path(spec_path)
        self.spec = self._load_spec()
    
    def _load_spec(self) -> Dict[str, Any]:
        """Load OpenAPI specification from file"""
        if self.spec_path.exists():
            with open(self.spec_path, 'r') as f:
                return yaml.safe_load(f)
        return {}
    
    def validate_endpoint(self, path: str, method: str, parameters: Dict[str, Any]) -> List[str]:
        """Validate endpoint parameters against OpenAPI spec"""
        errors = []
        
        # Get endpoint spec
        endpoint_spec = self.spec.get('paths', {}).get(path, {}).get(method.lower(), {})
        if not endpoint_spec:
            return [f"Endpoint {method} {path} not found in OpenAPI spec"]
        
        # Get parameter definitions
        spec_params = endpoint_spec.get('parameters', [])
        spec_param_names = {p['name'] for p in spec_params}
        
        # Check for missing required parameters
        for param in spec_params:
            if param.get('required', False) and param['name'] not in parameters:
                errors.append(f"Missing required parameter: {param['name']}")
        
        # Check for extra parameters not in spec
        for param_name in parameters:
            if param_name not in spec_param_names and param_name not in ['db']:
                errors.append(f"Parameter '{param_name}' not defined in OpenAPI spec")
        
        # Validate parameter types and constraints
        for param in spec_params:
            param_name = param['name']
            if param_name in parameters:
                value = parameters[param_name]
                schema = param.get('schema', {})
                
                # Check enum values
                if 'enum' in schema and value is not None:
                    if value not in schema['enum']:
                        errors.append(
                            f"Parameter '{param_name}' value '{value}' not in allowed values: {schema['enum']}"
                        )
                
                # Check numeric constraints
                if schema.get('type') == 'integer' and value is not None:
                    if 'minimum' in schema and value < schema['minimum']:
                        errors.append(f"Parameter '{param_name}' value {value} is less than minimum {schema['minimum']}")
                    if 'maximum' in schema and value > schema['maximum']:
                        errors.append(f"Parameter '{param_name}' value {value} is greater than maximum {schema['maximum']}")
        
        return errors
    
    def generate_fastapi_parameters(self, path: str, method: str) -> str:
        """Generate FastAPI parameter definitions from OpenAPI spec"""
        endpoint_spec = self.spec.get('paths', {}).get(path, {}).get(method.lower(), {})
        if not endpoint_spec:
            return ""
        
        params = []
        for param in endpoint_spec.get('parameters', []):
            name = param['name']
            schema = param.get('schema', {})
            param_type = self._get_python_type(schema)
            
            # Build parameter definition
            param_def = f"{name}: "
            
            # Add Optional if not required
            if not param.get('required', False):
                param_def += f"Optional[{param_type}] = Query(None"
            else:
                param_def += f"{param_type} = Query(..."
            
            # Add description
            if 'description' in param:
                param_def += f', description="{param["description"]}"'
            
            # Add constraints
            if 'enum' in schema:
                param_def += f", regex=\"^({'|'.join(schema['enum'])})$\""
            if 'minimum' in schema:
                param_def += f", ge={schema['minimum']}"
            if 'maximum' in schema:
                param_def += f", le={schema['maximum']}"
            if 'default' in schema:
                param_def += f", default={schema['default']}"
            
            param_def += ")"
            params.append(param_def)
        
        return ",\n    ".join(params)
    
    def _get_python_type(self, schema: Dict[str, Any]) -> str:
        """Convert OpenAPI schema type to Python type"""
        type_map = {
            'string': 'str',
            'integer': 'int',
            'number': 'float',
            'boolean': 'bool',
            'array': 'List',
            'object': 'Dict'
        }
        return type_map.get(schema.get('type', 'string'), 'Any')


# Singleton instance
openapi_compliance = OpenAPICompliance()


def ensure_openapi_compliance(func):
    """Decorator to ensure endpoint compliance with OpenAPI spec"""
    async def wrapper(request: Request, *args, **kwargs):
        # Extract path and method
        path = request.url.path
        method = request.method
        
        # Get parameters
        params = dict(request.query_params)
        params.update(kwargs)
        
        # Validate against spec
        errors = openapi_compliance.validate_endpoint(path, method, params)
        if errors:
            # Log validation errors (in production, you might want to raise exceptions)
            print(f"OpenAPI compliance errors for {method} {path}: {errors}")
        
        # Call original function
        return await func(request, *args, **kwargs)
    
    return wrapper
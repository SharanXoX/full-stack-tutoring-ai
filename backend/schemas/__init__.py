# Re-export everything from the parent schemas.py file
import importlib.util
import os

# Get the path to the parent schemas.py file
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
schemas_file = os.path.join(parent_dir, 'schemas.py')

# Load the schemas.py module
spec = importlib.util.spec_from_file_location("backend.schemas_module", schemas_file)
schemas_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(schemas_module)

# Re-export everything
SignupRequest = schemas_module.SignupRequest
LoginRequest = schemas_module.LoginRequest
TokenResponse = schemas_module.TokenResponse
UserOut = schemas_module.UserOut

__all__ = ['SignupRequest', 'LoginRequest', 'TokenResponse', 'UserOut']


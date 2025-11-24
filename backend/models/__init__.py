# Re-export everything from the parent models.py file
import importlib.util
import os

# Get the path to the parent models.py file
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
models_file = os.path.join(parent_dir, 'models.py')

# Load the models.py module
spec = importlib.util.spec_from_file_location("backend.models_module", models_file)
models_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(models_module)

# Re-export everything
BASE = models_module.BASE
User = models_module.User
Message = models_module.Message
HomeworkSession = models_module.HomeworkSession
QuizAttempt = models_module.QuizAttempt
QuizQuestion = models_module.QuizQuestion
get_engine = models_module.get_engine
create_tables = models_module.create_tables

__all__ = ['BASE', 'User', 'Message', 'HomeworkSession', 'QuizAttempt', 'QuizQuestion', 'get_engine', 'create_tables']

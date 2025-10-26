import os
from importlib import import_module
from pathlib import Path

# Get the directory containing this file
current_dir = Path(__file__).parent

# Get all .py files in the current directory
model_files = [
    f[:-3] for f in os.listdir(current_dir)
    if f.endswith('.py') 
    and f != '__init__.py'
    and not f.startswith('_')
]

# Import all models
for model in model_files:
    import_module(f'db.models.{model}')
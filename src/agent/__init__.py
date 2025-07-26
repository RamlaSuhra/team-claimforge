# __init__.py for the agent package
# This file allows the agent directory to be treated as a Python package.

#from agent import GeminiPatentAgent # Cleaner and more direct!
from .GeminiPatentAgent import GeminiPatentAgent # test Flask deployment/production 
# The above import exposes GeminiPatentAgent for use in other modules or for deployment 

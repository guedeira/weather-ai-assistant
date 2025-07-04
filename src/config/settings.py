import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')

DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')

if not OPENAI_API_KEY:
    print('Erro: Adicionar OPENAI_API_KEY no .env')
    exit(1)
    
if not OPENWEATHER_API_KEY:
    print('Erro: Adicionar OPENWEATHER_API_KEY no .env')
    exit(1)

OPENAI_MODEL = 'gpt-4.1-mini'
OPENAI_TEMPERATURE = 0.3
OPENAI_MAX_TOKENS = 100

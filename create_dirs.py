import os

dirs = [
    'app',
    'app/static',
    'app/static/uploads',
    'app/templates'
]

for dir in dirs:
    os.makedirs(dir, exist_ok=True)
    print(f'Created directory: {dir}')

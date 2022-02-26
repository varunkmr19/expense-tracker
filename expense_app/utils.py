from uuid import uuid4

def category_icon_directory_path(instance, filename: str) -> str:
  ''' Generate random filename and return directory path assets/category_icons/[filename] '''
  extension = filename.split('.')[-1]
  filename = f'{uuid4()}.{extension}'
  return f'assets/category_icons/{filename}'
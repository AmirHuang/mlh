from django.test import TestCase

# Create your tests here.
try:
    print(1/1)
except Exception:
    print('except')
else:
    print('else')
finally:
    print('finally')
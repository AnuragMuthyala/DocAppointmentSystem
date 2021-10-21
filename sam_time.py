from datetime import datetime

v = datetime.now().isoformat()
v = v.split('.')[0].split('T')
print(v)
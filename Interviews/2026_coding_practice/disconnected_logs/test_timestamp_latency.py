from collections import defaultdict
from datetime import datetime

a = datetime.fromisoformat('2026-03-14T09:00:00')
b = datetime.fromisoformat('2026-03-14T09:00:05')
diff = abs(a - b)
print(type(diff), diff.total_seconds())


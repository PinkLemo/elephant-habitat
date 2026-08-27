from slowapi import Limiter
from slowapi.util import get_remote_address

# One shared instance. Both main.py (for app.state + exception handler)
# and any route module using @limiter.limit(...) must import *this* object —
# creating a second Limiter() elsewhere would track requests separately
# and silently defeat the rate limiting.
limiter = Limiter(key_func=get_remote_address)
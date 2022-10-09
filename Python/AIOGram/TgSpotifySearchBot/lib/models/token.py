import time
from dataclasses import dataclass

@dataclass
class Token:
    access_token: str
    token_type: str
    expires_in: int

    @property
    def expiry(self):
        return int(time.time()) + self.expires_in

    @property
    def is_expired(self) -> bool:
        now = int(time.time())
        return self.expiry - now < 60
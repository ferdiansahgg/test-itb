import pyotp
import base64

shared_secret = "ii2210_sister_"
key = base64.b32encode(shared_secret.encode("utf-8")).decode("utf-8")
totp = pyotp.TOTP(s=key, digest="SHA256", digits=8)

print("Your OTP code is:", totp.now())

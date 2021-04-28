"""
2021: This code gives "Access denied (insufficient permissions) when the yubikey is plugged in. No good.
"""

import sys
import yubico

try:
    yubikey = yubico.find_yubikey()
    print("Version: {}".format(yubikey.version()))
except yubico.yubico_exception.YubicoError as e:
    print("ERROR: {}".format(e.reason))
    sys.exit(1)

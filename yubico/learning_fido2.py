# Copyright (c) 2018 Yubico AB
# All rights reserved.
#
#   Redistribution and use in source and binary forms, with or
#   without modification, are permitted provided that the following
#   conditions are met:
#
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""
Connects to the first FIDO device found (starts from USB, then looks into NFC),
creates a new credential for it, and authenticates the credential.
This works with both FIDO 2.0 devices as well as with U2F devices.
On Windows, the native WebAuthn API will be used.
"""
from __future__ import print_function, absolute_import, unicode_literals

from fido2.hid import CtapHidDevice
from fido2.client import Fido2Client, WindowsClient
from fido2.server import Fido2Server
from getpass import getpass
import sys
import ctypes
import pickle
from pathlib import Path

try:
    from fido2.pcsc import CtapPcscDevice
except ImportError:
    CtapPcscDevice = None


def enumerate_devices():
    for dev in CtapHidDevice.list_devices():
        yield dev
    if CtapPcscDevice:
        for dev in CtapPcscDevice.list_devices():
            yield dev


use_prompt = False
pin = None
uv = "discouraged"


def load_credentials():
    if not Path("credentials.pkl").exists():
        return []
    return pickle.load(open("credentials.pkl", "rb"))


def dump_credentials(credentials):
    pickle.dump(credentials, open("credentials.pkl", "wb"))


def get_client():
    global use_prompt
    if WindowsClient.is_available() and not ctypes.windll.shell32.IsUserAnAdmin():
        # Use the Windows WebAuthn API if available, and we're not running as admin
        client = WindowsClient("https://example.com")
    else:
        # Locate a device
        for dev in enumerate_devices():
            client = Fido2Client(dev, "https://example.com")
            if client.info.options.get("rk"):
                use_prompt = not (CtapPcscDevice and isinstance(dev, CtapPcscDevice))
                break
        else:
            print("No Authenticator with support for resident key found!")
            sys.exit(1)

        # Prefer UV if supported
        if client.info.options.get("uv"):
            uv = "preferred"
            print("Authenticator supports User Verification")
        elif client.info.options.get("clientPin"):
            # Prompt for PIN if needed
            pin = getpass("Please enter PIN: ")
        else:
            print("PIN not set, won't use")
    return client


def add_credentials(server, client):
    user = {"id": b"user_id", "name": "A. User"}

    # Prepare parameters for makeCredential
    create_options, state = server.register_begin(
        user,
        resident_key=True,
        user_verification=uv,
        authenticator_attachment="cross-platform",
    )

    # Create a credential
    if use_prompt:
        print("\nTouch your authenticator device now...\n")

    result = client.make_credential(create_options["publicKey"], pin=pin)

    # Complete registration
    auth_data = server.register_complete(
        state, result.client_data, result.attestation_object
    )
    credentials = load_credentials()
    if auth_data.credential_data not in credentials:
        credentials.append(auth_data.credential_data)
        dump_credentials(credentials)

    print("New credential created!")

    print("CLIENT DATA:", result.client_data)
    print("ATTESTATION OBJECT:", result.attestation_object)
    print()
    print("CREDENTIAL DATA:", auth_data.credential_data)
    return credentials


def authenticate_device(server, client):
    # Prepare parameters for getAssertion
    request_options, state = server.authenticate_begin(user_verification=uv)

    # Authenticate the credential
    if use_prompt:
        print("\nTouch your authenticator device again...\n")

    selection = client.get_assertion(request_options["publicKey"], pin=pin)
    result = selection.get_response(0)  # There may be multiple responses, get the first.

    print("USER ID:", result.user_handle)

    credentials = load_credentials()
    # Complete authenticator
    server.authenticate_complete(
        state,
        credentials,
        result.credential_id,
        result.client_data,
        result.authenticator_data,
        result.signature,
    )

    print("Credential authenticated!")

    print("CLIENT DATA:", result.client_data)
    print()
    print("AUTHENTICATOR DATA:", result.authenticator_data)


def main():
    server = Fido2Server({"id": "example.com", "name": "Example RP"}, attestation="direct")
    client = get_client()
    # add_credentials(server, client)
    authenticate_device(server, client)


if __name__ == "__main__":
    main()

import hmac
import hashlib
import os
from .models import Providers, Clients


def sign(client_name):

    client = Clients.objects.get(name=client_name)
    random_input = os.urandom(64).hex()
    hash_object = hashlib.sha256(random_input.encode())
    hash_hex = hash_object.hexdigest()

    try:
        provider = Providers.objects.get(client=client)
        provider.signature = hash_hex
        provider.save()
    except:
        provider = Providers.objects.create(client=client, signature=hash_hex)
        provider.save()

    return hash_hex

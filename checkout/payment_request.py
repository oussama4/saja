import hashlib
import base64


def generateHash(attributes):

    ordredAttValues = [attributes.get(v,'') for v in sorted(attributes)]
    toHash = "|".join((ordredAttValues))

    h = hashlib.sha512()
    h.update(toHash.encode())

    attributes['hash']=base64.b64encode(h.digest())

    return attributes




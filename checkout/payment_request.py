import hashlib
import base64


def generateHash(attributes):

    ordredAttValues = [attributes.get(v,'') for v in sorted(attributes)]
    toHash = "|".join((ordredAttValues))

    h = hashlib.sha512()
    h.update(toHash.encode())

    attributes['hash']=base64.b64encode(h.digest())
    print(attributes['hash'].decode())
    return attributes


d={
        'amount':"44",
        'clientid': "44445",
        'billing': "154",
}

generateHash(d)



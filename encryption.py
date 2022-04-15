import os
import tempfile
import base64
import json
import uuid

def os_test():
    ret = os.system('echo "hello"')
    print(ret)

# os_test()

def test_encrypt():
    data = {
        'hello': 1,
        'bob': 2,
        'fishing': 3
    }

    js = json.dumps(data, indent=4)

    with tempfile.NamedTemporaryFile() as b64_log:
        b64_json = base64.b64encode(bytes(js, 'utf-8'))
        b64_log.write(b64_json)

        key = 'fishing-in-the-river-champion!'

        os.system(f'openssl enc -aes-128-cbc -in {b64_log.name} -out logs.json -k {key} -md sha256')

# test_encrypt()

def direct():
    data = {
        'vip': 1,
        'bird': 2,
        'dog': 3
    }

    js = json.dumps(data, indent=4)
    key = 'fishing-in-the-river-champion!'

    with tempfile.NamedTemporaryFile(mode='w') as b64_log:
        b64_log.write(js)
        os.system(f'openssl enc -aes-128-cbc -in {b64_log.name} -base64 -out logs.json -k {key} -md sha256')

# direct()

def uuid_test():
    data = {
        'hello': 1,
        'bob': 2,
        'fishing': 3
    }

    js = json.dumps(data, indent=4)
    key = 'fishing-in-the-river-champion!'

    unique_name = str(uuid.uuid4())
    with open(unique_name, 'w') as f:
        f.write(js)
    
    os.system(f'cat {unique_name}')
    os.system(f'openssl enc -aes-128-cbc -in {unique_name} -base64 -out logs.json -k {key} -md sha256')
    os.remove(unique_name)

uuid_test()

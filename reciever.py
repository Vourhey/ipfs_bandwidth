import ipfsapi
from base64 import b64decode
from json import loads
from threading import Thread
from time import sleep, time

TOPIC = "airalab.measure.ipfs.bandwidth"

def get_from_ipfs(client, msg, n_list):
    n_list.append(client.cat(msg).decode('utf-8'))

def subscribe(IPFS):
    with IPFS.pubsub_sub(TOPIC) as sub:
        for msg in sub:
            try:
                yield b64decode(msg['data']).decode('utf-8')
            except Exception as e:
                print("IPFS Client sub error: {}".format(e))

def read_channel(ipfs_client, hash_list, number_list):
    for m in subscribe(ipfs_client):
        hash_list.append(m)
        Thread(target=get_from_ipfs, kwargs={'client': ipfs_client, 'msg': m, 'n_list': number_list}, daemon=True).start()

if __name__ == '__main__':
    IPFS = ipfsapi.Client()
    h_list = []
    n_list = []

    Thread(target=read_channel, kwargs={'ipfs_client': IPFS, 'hash_list': h_list, 'number_list': n_list}, daemon=True).start()
    current_time = time()
    while True:

        sleep(0.1)
        print(len(h_list))

        if len(h_list) == 1000:
            with open('recieved.txt', 'w') as f:
                f.write('\n'.join(n_list))
                f.close()
            print(time() - current_time)
            break


import ipfsapi
import random

TOPIC = "airalab.measure.ipfs.bandwidth"

if __name__ == '__main__':
    ipfs = ipfsapi.Client()
    numbers = []

    for n in range(0, 1000):
        data = random.randint(1, 2**32)
        # print(data)
        ipfs_hash = ipfs.add_str(str(data))
        numbers.append(data)

        ipfs.pubsub_pub(TOPIC, ipfs_hash)

    with open('spammed.txt', 'w') as f:
        f.write('\n'.join(map(str, numbers)))
        f.close()


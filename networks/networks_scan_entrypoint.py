import threading
import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from eventscanner.queue.pika_handler import send_to_backend
from networks.duc import DucMaker
from settings.settings_local import NETWORKS

networks = {
    'DUCATUS_MAINNET': DucMaker
}


class ScanEntrypoint(threading.Thread):

    def __init__(self, network_name, network_maker, polling_interval, commitment_chain_length):
        super().__init__()
        self.network = network_maker(network_name, polling_interval, commitment_chain_length)

    def run(self):
        self.network.scanner.poller()


if __name__ == '__main__':
    for network_name, network_maker in networks.items():
        scan = ScanEntrypoint(network_name, network_maker, NETWORKS[network_name]['polling_interval'],
                              NETWORKS[network_name]['commitment_chain_length'])
        scan.start()
        send_to_backend(network_name, NETWORKS[network_name]['queue'], {})

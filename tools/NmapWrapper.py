class NmapWrapper:
    def __init__(self, nmap_path: str = "nmap"):
        self.nmap_path = nmap_path

    @staticmethod
    def scan():
        import nmap as scanner

        scanner = scanner.PortScanner()
        scanner.scan(hosts='192.168.178.1/24', arguments='-n -sP -PE -PA21,23,80,3389')
        hosts_list = [(x, scanner[x]['status']['state']) for x in scanner.all_hosts()]
        print(hosts_list)
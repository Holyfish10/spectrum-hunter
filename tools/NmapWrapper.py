class NmapWrapper:
    def __init__(self, nmap_path: str = "nmap"):
        self.nmap_path = nmap_path

    def scan(self, target: str, arguments: str = ''):
        import nmap as scanner

        scanner = scanner.PortScanner()
        scanner.scan(hosts=target, arguments=arguments)
        hosts_list = [(x, scanner[x]['status']['state']) for x in scanner.all_hosts()]
        print(hosts_list)
        return hosts_list

    @staticmethod
    def flags_to_arguments(flags):
        """
        Takes a list of flags like ['-sS', '-sV'] and returns a single argument string: '-sS -sV'
        """
        if isinstance(flags, list):
            return " ".join(flags)
        return str(flags)

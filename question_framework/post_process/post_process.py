from ipaddress import ip_address

def ip_range_to_list(x):
    def ip_range_generator(ip1, ip2):
        ip1 = int(ip_address(ip1))
        ip2 = int(ip_address(ip2))
        ip1, ip2 = min(ip1, ip2), max(ip1, ip2)
        for i in range(ip1, ip2 + 1):
            yield ip_address(i)
    ip1, ip2 = x.replace(" ", "").split("-")

    return ip_range_generator(ip1, ip2)
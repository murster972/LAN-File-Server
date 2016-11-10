def valid_ip_addr(ip):
    'checks that the user has entered a valid ip address'
    quads = ip.split(".")

    try:
        a = int("".join(quads))
        if len(quads) == 4:
            for i in quads:
                if int(i) > 255 or int(i) < 0:
                    return False
            return True
        else:
            return False
    except ValueError:
        return False

while True:
    x = input("IP: ")
    print(valid_ip_addr(x))

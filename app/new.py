from growwapi import *

app  = GrowwApi()

def get_live_feed():
    feed = app.get_live_feed()
    print(feed)


def towerhon(n, source, destination, temp):
    if n == 1:
        print("Move disk 1 from rod", source, "to rod", destination)
        return
    
    # Move n-1 disks from source to temp
    towerhon(n - 1, source, temp, destination)

    # Move nth disk to destination
    print("Move disk", n, "from rod", source, "to rod", destination)

    # Move n-1 disks from temp to destination
    towerhon(n - 1, temp, destination, source)

if __name__ == "__main__":
    n =1
    towerhon(n, 'A', 'B', 'C')

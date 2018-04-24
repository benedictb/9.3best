import app.db


def deserialize(str):
    return {item.split('=')[0]: item.split('=')[1] for item in str.split('&')}


def weekList():
    return ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat']
    # Return

# NEED TO FIX SOMEHOW
def getDays(bitstring):
    return [True for _ in range(7)]


def getRandomTimes():
    start = ' ' + str(random.randint(1, 11)) + ':' + str(random.randint(0, 59)) + ':' + str(random.randint(0, 59))
    stop = ' ' + str(random.randint(12, 23)) + ':' + str(random.randint(0, 59)) + ':' + str(random.randint(0, 59))
    return start, stop
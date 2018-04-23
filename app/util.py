import app.db


def deserialize(str):
    return {item.split('=')[0]: item.split('=')[1] for item in str.split('&')}


def dayOfWeek(datetime):
    return ['sun', 'mon', 'tue', 'wed', 'thur', 'fri', 'sat']
    # Return

# NEED TO FIX SOMEHOW
def getDays(bitstring):
    return [True for _ in range(7)]
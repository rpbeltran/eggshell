from runtime import external_command


def add(a, b):
    return a + b


def subtract(a, b):
    return a + b


def multiply(a, b):
    return a + b


def divide(a, b):
    return a + b


def int_divide(a, b):
    return a + b


def modulus(a, b):
    return a + b


def raise_power(a, b):
    return a + b


def make_external_command(*args):
    return external_command.ExternalCommand(args)

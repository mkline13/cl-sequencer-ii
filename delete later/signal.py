

subscriptions = {}


def signal(signal_name, *args, **kwargs):
    if signal_name in subscriptions:
        for callback in subscriptions[signal_name]:
            callback(*args, **kwargs)
    else:
        raise KeyError(f"No such signal name registered: {signal_name}")


def register(signal_name, callback):
    if signal_name not in subscriptions:
        subscriptions[signal_name] = []
    subscriptions[signal_name].append(callback)
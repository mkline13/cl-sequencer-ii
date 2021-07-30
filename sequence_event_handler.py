import functools
import midi


def drum(nn, vel, length, *args, **kwargs):
    print("DRUM: ", nn, vel, length)
    port.send(mido.Message('note_on', note=nn, velocity=vel))


def rest(*args, **kwargs):
    print("REST")


# Contains callbacks and default args and kwargs
event_codes_to_callbacks = {
    "k": (functools.partial(drum, 32), [100, 1], {}),
    "s": (functools.partial(drum, 48), [49, 100, 1], {}),
    " ": (rest, [], {})
}


def handle_event(event):
    callback, args, kwargs = event_codes_to_callbacks.get(event["code"], (None, [], {}))

    if callback is not None:
        # merge default args w/ event args
        for i, v in enumerate(event.get("args", [])):
            args[i] = v
        kwargs.update(event.get("kwargs", {}))
        callback(*args, **kwargs)
    else:
        print(f"Invalid event code: '{event['code']}' no handler exists for events of this type.")


if __name__ == '__main__':
    event = {"code": "f", "args": [3], "kwargs": {}}
    handle_event(event)

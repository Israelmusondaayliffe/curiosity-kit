"""Protocol-2 state access. Raw v1 transition setters are deliberately superseded.

Use Runtime.prepare/begin_launch/record_launch/ingest for all execution modes,
Runtime.cancel for stop requests, Runtime.settle for observations and finalize for
terminal success. A caller-supplied status or readiness boolean grants no authority.
"""
from .storage import ConversionNeeded, RuntimeErrorBase

class IllegalTransitionError(RuntimeErrorBase):
    pass

class RetryRejectedError(IllegalTransitionError):
    pass


def replay_events(events):
    raise ConversionNeeded("v1 event replay superseded by Runtime.replay() over protocol-2 committed operations")


class StateMachine:
    def __init__(self, run_directory, state=None, event_store=None):
        from .runtime import Runtime
        self.runtime = Runtime(run_directory)

    @classmethod
    def create(cls, *args, **kwargs):
        raise ConversionNeeded("use Runtime.create; v1 state creation cannot authorize a v2 run")

    @classmethod
    def resume(cls, run_directory, event_store=None):
        obj = cls(run_directory)
        obj.runtime.recover()
        return obj

    @property
    def state(self):
        return self.runtime.load()

    def transition_node(self, *args, **kwargs):
        raise ConversionNeeded("raw transition superseded: guarded Runtime lifecycle required")

    def complete_run(self, **kwargs):
        kwargs.pop("timestamp",None)
        kwargs.pop("actor_node_id",None)
        return self.runtime.finalize(**kwargs)

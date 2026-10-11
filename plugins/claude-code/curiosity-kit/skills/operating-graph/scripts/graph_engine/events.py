"""Committed operation history, with no unguarded append entry point."""
from .storage import Store, CorruptionError, ConversionNeeded

class EventChainError(CorruptionError):
    pass

class WriterAuthorityError(PermissionError):
    pass


class EventStore:
    def __init__(self, run_directory, run_id, *, controller_node_id="controller"):
        self.store = Store(run_directory)
        self.run_directory = self.store.root
        self.run_id = run_id
        self.controller_node_id = controller_node_id

    def require_controller(self, actor_node_id):
        if actor_node_id != self.controller_node_id:
            raise WriterAuthorityError("controller is sole logical writer; label is not authentication")

    def read_all(self):
        data,records = self.store.load()
        if data["runId"] != self.run_id:
            raise EventChainError("run identity mismatch")
        return tuple(records)

    def append(self,*args,**kwargs):
        raise ConversionNeeded("raw event append superseded by guarded Runtime operations")

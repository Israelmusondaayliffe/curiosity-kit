"""Read-only criterion-specific verification. Explicit finalize is separate."""
from .storage import RuntimeErrorBase, CorruptionError

class VerificationError(RuntimeErrorBase):
    pass
class VerificationCorruptionError(CorruptionError):
    pass

class Verifier:
    def __init__(self,run_directory):
        from .runtime import Runtime
        self.runtime = Runtime(run_directory)

    def verify(self,**kwargs):
        if kwargs:
            raise VerificationError("verify is read-only and takes no timestamp/authority override")
        return self.runtime.verify()

    def finalize(self,**kwargs):
        return self.runtime.finalize(**kwargs)

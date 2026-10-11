"""Invocation-owned artifact access; activation is atomic with validated return."""
from pathlib import Path
from .storage import RuntimeErrorBase, CorruptionError, ConversionNeeded, identifier, safe_path

class ArtifactError(RuntimeErrorBase):
    pass
class UnsafeArtifactPathError(ArtifactError):
    pass
class ArtifactIntegrityError(CorruptionError):
    pass
class ArtifactUnavailableError(ArtifactError):
    pass


def resolve_artifact_path(run_directory,node_id,relative_path):
    identifier(node_id,"nodeId")
    if not isinstance(relative_path,str) or not relative_path.startswith("artifacts/"+node_id+"/"):
        raise UnsafeArtifactPathError("artifact path outside node ownership")
    try:
        return safe_path(Path(run_directory),relative_path)
    except RuntimeErrorBase as exc:
        raise UnsafeArtifactPathError(str(exc)) from exc


class ArtifactRegistry:
    def __init__(self,run_directory,run_id=None,event_store=None):
        from .runtime import Runtime
        self.runtime = Runtime(run_directory)
        self.run_directory = self.runtime.root
        if run_id is not None and self.runtime.load()["runId"] != run_id:
            raise ArtifactIntegrityError("run identity mismatch")

    def read_all(self):
        return tuple(self.runtime.load()["artifacts"].values())

    def verify(self,artifact_id,*,require_active=True):
        data = self.runtime.load()
        art = data["artifacts"].get(artifact_id)
        if not art or (require_active and (not art["active"] or data["graphVersion"] not in art["eligibleVersions"])):
            raise ArtifactUnavailableError("artifact missing or inactive")
        self.runtime._verify_artifact(art)
        return art

    def active_artifacts(self,artifact_type=None):
        return tuple(self.runtime._active(self.runtime.load(),artifact_type=artifact_type))

    def satisfies_activation(self,*args,**kwargs):
        raise ConversionNeeded("global type matching cannot establish lineage; use Runtime.ready")

    def register(self,*args,**kwargs):
        raise ConversionNeeded("standalone artifact activation superseded by Runtime.ingest")

    def invalidate(self,*args,**kwargs):
        raise ConversionNeeded("use guarded Runtime rewrite invalidation; raw artifact mutations unsupported")

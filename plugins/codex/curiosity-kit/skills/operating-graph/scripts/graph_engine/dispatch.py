"""Protocol-2 fresh-worker dispatch facade; no legacy persistence bypass.

The controller calls prepare, then begin_launch, translates launchSpec into its
actual available host tool, and persists the observed response. The runtime never
pretends a JSON receipt or role label authenticates a native worker.
"""
from pathlib import Path
import hashlib
from .storage import RuntimeErrorBase, ConversionNeeded

PROTOCOL_VERSION = 2
TASK_PACKET_TYPE = "NodeTaskPacket"
LAUNCH_RECORD_TYPE = "ThreadLaunchRecord"
RETURN_PACKET_TYPE = "NodeReturnPacket"
DISPATCH_RECEIPT_TYPE = "DispatchReceipt"
LAUNCH_RECEIPT_TYPE = "LaunchReceipt"

class PacketValidationError(RuntimeErrorBase):
    pass


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _obsolete(*args,**kwargs):
    raise ConversionNeeded("v1 dispatch signature superseded: use Runtime.prepare, begin_launch, record_launch, ingest")

prepare_dispatch = _obsolete
record_launch = _obsolete
ingest_return = _obsolete
preview_dispatch = _obsolete


def thread_history_issues(run_directory,graph=None,state=None):
    from .runtime import Runtime
    try:
        Runtime(run_directory).load()
    except RuntimeErrorBase as exc:
        return [str(exc)]
    return []


def thread_evidence_summary(run_directory,graph=None,state=None):
    from .runtime import Runtime
    data = Runtime(run_directory).load()
    return [{"invocationId":i["invocationId"],"nodeId":i["nodeId"],"status":i["status"],
             "graphVersion":i["graphVersion"],"epoch":i["epoch"],"attempt":i["attempt"],
             "launchReceipt":i["launchReceipt"],"returned":i["returned"] is not None}
            for i in data["invocations"].values()]

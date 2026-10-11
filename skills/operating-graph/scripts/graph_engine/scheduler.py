"""Authoritative readiness facade. Ordering is retained in Runtime._ready.

A graph plus caller-authored state is planning data, never execution authority.
Readiness must use the same committed loader as launch and return ingestion.
"""
from dataclasses import dataclass
from .storage import ConversionNeeded

@dataclass(frozen=True)
class DeadlockReport:
    blocked_node_ids: tuple
    reason: str = "no dependency-ready work; inspect exact blockers and obligations"


def get_ready_nodes(graph,state,*,artifact_registry=None,approvals=(),detected_available_worker_slots=None,fixed_agent_limit=None):
    if artifact_registry is None or approvals:
        raise ConversionNeeded("readiness needs committed Runtime; imported approvals do not grant authority")
    rt = artifact_registry.runtime
    slots = detected_available_worker_slots
    if fixed_agent_limit is not None:
        slots = min(slots if slots is not None else fixed_agent_limit, max(0,fixed_agent_limit-1))
    ready = rt.ready(available_slots=slots)["readyNodeIds"]
    return tuple(n for key in ready for n in graph.nodes if n.id == key)


def concurrency_limit(*args,**kwargs):
    raise ConversionNeeded("use Runtime.ready capacity, including outstanding reservations")


def can_advance_epoch(*args,**kwargs):
    raise ConversionNeeded("use Runtime.advance_epoch; state-only epoch predicates are not authoritative")


def detect_deadlock(graph,state,*,artifact_registry=None,approvals=()):
    if artifact_registry is None or approvals:
        raise ConversionNeeded("use Runtime.status blockers and obligations")
    result = artifact_registry.runtime.status()
    if result["readyNodeIds"] or result["obligations"] or result["state"]["status"] != "running":
        return None
    return DeadlockReport(tuple(sorted(result["blockers"])))

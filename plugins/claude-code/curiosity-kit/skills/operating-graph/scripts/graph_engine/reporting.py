"""Deterministic text, JSON, and Mermaid reporting."""

from __future__ import annotations

import json
import re

from .models import Graph, RuntimeState, VerificationResult


def render_json(result: VerificationResult) -> str:
    """Render canonical machine-readable verification output."""
    return json.dumps(
        result.to_dict() if hasattr(result, "to_dict") else result,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )


def render_text(result) -> str:
    """Render either v1 value objects or protocol-2 verification dictionaries."""
    data = result.to_dict() if hasattr(result, "to_dict") else result
    lines = [f"Verification: {data['status']}", f"Checked: {data['checkedAt']}"]
    for item in data.get("criteria", []):
        lines.append(f"- [{'pass' if item.get('satisfied') else 'fail'}] {item.get('criterion', 'unnamed criterion')}")
    lines.extend("- " + issue for issue in data.get("issues", []))
    for item in data.get("omittedNodes", []):
        lines.append(f"- Omitted {item['nodeId']}: {item['reason']}; prior outcomes: {', '.join(item['priorOutcomes']) or 'none'}")
    return "\n".join(lines) + "\n"


def render_runtime_text(status) -> str:
    data = status["state"]
    limit = data["graph"]["limits"]
    lines = [f"Run: {data['runId']}", f"Graph: {data['graph']['name']} (version {data['graphVersion']}, epoch {data['epoch']})",
             f"Status: {data['status']}; generation: {data['generation']}",
             f"Issued launch attempts: {data['launchAttempts']}/{min(limit['maxNodeRuns'],data['contract']['maxLaunchAttempts'])}; recorded as launched (any lane, not proof of a separate worker): {data['totalNodeRuns']}",
             f"Deadline: {data['contract']['deadline']}",
             "Ready: " + (", ".join(status["readyNodeIds"]) or "none"),
             "Outstanding obligations: " + (", ".join(status["obligations"]) or "none"), "Nodes:"]
    for key,node in sorted(data["nodes"].items()):
        lines.append(f"- {key}: {node['status']}; attempts {node['attempts']}")
        if key in status["blockers"]:
            lines.append("  " + "; ".join(status["blockers"][key]))
    lines.append(f"Artifacts: {sum(a['active'] for a in data['artifacts'].values())} active / {len(data['artifacts'])} retained")
    lines.append(f"Approval decisions: {len(data['approvals'])}; applied rewrites: {len(data['rewrites'])}; pending boundary: {data['rewritePending']}")
    lines.append(f"Evidence tier: {data['contract']['evidenceTier']}; native qualification is separate")
    return "\n".join(lines) + "\n"


def _mermaid_id(value: str) -> str:
    normalized = re.sub(r"[^A-Za-z0-9_]", "_", value)
    if normalized and normalized[0].isdigit():
        normalized = f"n_{normalized}"
    return normalized or "node"


def _label(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', "\\\"")


def render_mermaid(graph: Graph, state=None, result=None) -> str:
    """Render topology and either v1 value state or protocol-2 committed state."""
    if state is None:
        statuses = {}
    elif isinstance(state, dict):
        statuses = {key:value["status"] for key,value in state["nodes"].items()}
    else:
        statuses = {key:value.status.value for key,value in state.node_states.items()}
    verdict = result.get("status", "not-checked") if isinstance(result, dict) else result.status.value if result is not None else "not-checked"
    lines = ["flowchart TD"]
    ids = {node.id: _mermaid_id(node.id) for node in graph.nodes}
    for node in sorted(graph.nodes, key=lambda item:item.id):
        status = statuses.get(node.id,"not-started")
        lines.append(f'    {ids[node.id]}["{_label(node.label)}\\n{status}"]')
    for edge in sorted(graph.edges,key=lambda item:item.id):
        if edge.enabled:
            lines.append(f"    {ids[edge.source]} --> {ids[edge.target]}")
    palette = {"succeeded":"fill:#dcfce7,stroke:#166534","failed":"fill:#fee2e2,stroke:#991b1b",
               "blocked":"fill:#fef3c7,stroke:#92400e","running":"fill:#dbeafe,stroke:#1d4ed8"}
    for status in sorted(set(statuses.values())):
        class_name = _mermaid_id(status)
        lines.append(f"    classDef {class_name} {palette.get(status,'fill:#f3f4f6,stroke:#4b5563')}")
    for node in sorted(graph.nodes,key=lambda item:item.id):
        if node.id in statuses:
            lines.append(f"    class {ids[node.id]} {_mermaid_id(statuses[node.id])}")
    lines.append(f"    %% verification: {verdict}")
    return "\n".join(lines) + "\n"


__all__ = ["render_json", "render_mermaid", "render_text", "render_runtime_text"]

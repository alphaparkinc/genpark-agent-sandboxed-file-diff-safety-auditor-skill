import json, sys
from client import AgentSandboxedFileDiffSafetyAuditorClient

def handle_mcp_request(payload):
    method = payload.get("method")
    req_id = payload.get("id", 1)
    if method == "initialize":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"protocolVersion": "2024-11-05", "serverInfo": {"name": "agent-sandboxed-file-diff-safety-auditor", "version": "1.0.0"}}}
    elif method == "tools/list":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": [{"name": "audit_code_diff", "description": "Audits agent code diffs for destructive commands, raw secret leaks, and security violations."}]}}
    elif method == "tools/call":
        client = AgentSandboxedFileDiffSafetyAuditorClient()
        res = client.audit_code_diff()
        return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
    return {"jsonrpc": "2.0", "id": req_id, "result": {"status": "ACTIVE"}}

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print(json.dumps(handle_mcp_request({"method": "tools/list"})))
    else:
        client = AgentSandboxedFileDiffSafetyAuditorClient()
        print(json.dumps(client.audit_code_diff(), indent=2))

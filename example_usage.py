import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from client import AgentSandboxedFileDiffSafetyAuditorClient

def main():
    client = AgentSandboxedFileDiffSafetyAuditorClient()
    res = client.audit_code_diff()
    print("=== Agent Sandboxed File Diff Safety Auditor Output ===")
    print(f"Target: {res['target_file']} | Safety Score: {res['safety_score']}/100")
    print(f"Safe to Apply: {res['is_safe_to_apply']} | Verdict: {res['verdict']}")
    print(f"Action: {res['recommended_agent_action']}")
    if res['violations_detected']:
        print("\nViolations Flagged:")
        for v in res['violations_detected']:
            print(f"  * [{v['violation']}] {v['line_content']}")

if __name__ == '__main__':
    main()

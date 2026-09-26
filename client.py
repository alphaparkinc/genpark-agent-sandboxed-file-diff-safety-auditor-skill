import json
import re
from typing import Dict, Any, List, Optional

class AgentSandboxedFileDiffSafetyAuditorClient:
    """
    Production-grade agent code edit and destructive diff safety auditor.
    Pre-audits file diffs, detects hardcoded secrets, dangerous subprocess commands,
    and flags critical destructive modifications before workspace disk writes.
    """
    def __init__(self):
        self.dangerous_patterns = [
            (re.compile(r"rm\s+-rf\s+[/~]", re.IGNORECASE), "ROOT_DIRECTORY_PURGE"),
            (re.compile(r"DROP\s+TABLE|DROP\s+DATABASE", re.IGNORECASE), "DATABASE_DESTRUCTION"),
            (re.compile(r"ghp_[A-Za-z0-9_]{36}|sk-[A-Za-z0-9_-]{32,}", re.IGNORECASE), "RAW_API_SECRET_LEAK"),
            (re.compile(r"chmod\s+777|chmod\s+-R\s+777", re.IGNORECASE), "OVERLY_PERMISSIVE_CHMOD")
        ]

    def audit_code_diff(
        self,
        target_file: str = "src/database/migration.py",
        diff_payload: Optional[str] = None
    ) -> Dict[str, Any]:
        if not diff_payload:
            diff_payload = """
+ import os
+ def purge_old_data():
+     api_key = "sk-live-9921448210984129841298412"
+     os.system("rm -rf /tmp/cache_old")
+     # Safe modification
+     return True
"""

        detected_violations = []
        lines = diff_payload.split("\n")
        added_lines = [l for l in lines if l.startswith("+") and not l.startswith("+++")]

        for line in added_lines:
            for pattern, violation_tag in self.dangerous_patterns:
                if pattern.search(line):
                    detected_violations.append({
                        "violation": violation_tag,
                        "line_content": line.strip()[:60]
                    })

        is_safe = len(detected_violations) == 0
        safety_score = max(0, 100 - (len(detected_violations) * 45))

        verdict = "APPROVE_SAFE_DIFF" if is_safe else "QUARANTINE_DIFF_BLOCK_WRITE"

        return {
            "audit_id": "diff_aud_7718",
            "target_file": target_file,
            "total_diff_lines_evaluated": len(added_lines),
            "safety_score": safety_score,
            "is_safe_to_apply": is_safe,
            "verdict": verdict,
            "violations_detected": detected_violations,
            "recommended_agent_action": "PERMIT_FILE_WRITE" if is_safe else "REJECT_AND_REQUEST_REDACTED_DIFF"
        }

import unittest
from pathlib import Path


RULES_PATH = Path(__file__).resolve().parents[1] / "cursor.list"


def load_rules():
    rules = []
    for raw in RULES_PATH.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line and not line.startswith("#"):
            rules.append(line)
    return rules


def matches_host(rule, host):
    kind, value = rule.split(",", 1)
    if kind == "DOMAIN":
        return host == value
    if kind == "DOMAIN-SUFFIX":
        return host == value or host.endswith("." + value)
    return False


class CursorListTest(unittest.TestCase):
    def test_cursor_production_hosts_are_covered(self):
        rules = load_rules()
        hosts = (
            "api2.cursor.sh",
            "agent.api5.cursor.sh",
            "prod.authentication.cursor.sh",
            "downloads.cursor.com",
            "marketplace.cursorapi.com",
            "cursor-cdn.com",
            "cursor-marketplace.com",
            "www.cursor.so",
            "agent.cursorvm.com",
            "cursor.blob.core.windows.net",
            "anysphere-binaries.s3.us-east-1.amazonaws.com",
        )
        for host in hosts:
            self.assertTrue(
                any(matches_host(rule, host) for rule in rules if rule.startswith("DOMAIN")),
                host,
            )

    def test_mac_process_paths_are_covered(self):
        rules = load_rules()
        self.assertIn("PROCESS-NAME,/Applications/Cursor.app/", rules)
        self.assertIn(
            "PROCESS-NAME,/Users/bing/.local/share/cursor-agent/",
            rules,
        )

    def test_shared_infrastructure_is_not_claimed(self):
        rules = load_rules()
        shared_hosts = (
            "github.com",
            "npmjs.org",
            "vercel-storage.com",
            "workos.com",
            "s3.amazonaws.com",
            "vscode-cdn.net",
        )
        for host in shared_hosts:
            self.assertFalse(
                any(matches_host(rule, host) for rule in rules if rule.startswith("DOMAIN")),
                host,
            )


if __name__ == "__main__":
    unittest.main()

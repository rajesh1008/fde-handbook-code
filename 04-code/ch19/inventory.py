"""Listing 19.1: score every way in and out of three customers' systems, and list what is still unknown."""
import _paths  # noqa: F401
from fieldkit.connectors import Surface, inventory_report, best_path

S = [
    Surface("caldwell claims-core", "reporting replica view", "db_view", "read", "Ruth Calloway", True,
            "claims platform on-call", "quarterly release notes", 1),
    Surface("caldwell claims-core", "nightly warehouse extract", "file_export", "read", "Ruth Calloway", True,
            "warehouse team", None, 2),
    Surface("caldwell claims-core", "first-notice screens FNOL-1/2", "screen_robotic", "write", "Anne Kessler",
            True, "claims platform on-call", "vendor patch notes", 2),
    Surface("caldwell claims-core", "vendor bulk loader (fixed width)", "batch_loader", "write", None, False,
            None, None, 0),
    Surface("caldwell intake", "claims intake mailbox", "mail", "read", "Anne Kessler", True, "messaging team",
            None, 0),
    Surface("caldwell intake", "scanning vendor SFTP drop", "file_export", "read", None, True, None, None, 0),
    Surface("caldwell intake", "fax server folder", "file_export", "read", "telecom team", True, None, None, 0),
    Surface("greystone ehr", "EHR print-to-file", "file_export", "read", "Ravi Shah", False, "Ravi Shah",
            "EHR upgrade calendar", 2),
    Surface("greystone ehr", "EHR inbound document interface", "queue", "write", "Ravi Shah", False,
            "Ravi Shah", "EHR release notes", 1),
    Surface("greystone ehr", "EHR referral screens", "screen_robotic", "read", "Michael Hart", False, None,
            "EHR upgrade calendar", 2),
    Surface("greystone intake", "fax server drop", "file_export", "read", "Ravi Shah", False, "Ravi Shah", None, 0),
    Surface("greystone payers", "payer portals (status only)", "screen_agent", "read", None, False, None, None, 5),
    Surface("pennant tms", "nightly status CSV via MFT", "file_export", "read", "Kofi Mensah", True,
            "MFT on-call", None, 2),
    Surface("pennant tms", "carrier EDI 214 via VAN", "queue", "read", "Kofi Mensah", True, "EDI desk",
            "partner onboarding notice", 3),
    Surface("pennant tms", "status update screen", "screen_robotic", "write", "Kofi Mensah", False, None,
            None, 1),
    Surface("pennant intake", "scanned and photographed forms share", "file_export", "read", "Jenna Ruiz", True,
            None, None, 0),
]

print(f"{'system':22} {'dir':5} {'surface':36} {'kind':15} score  unknown")
for sys_, d, name, kind, score, gaps in inventory_report(S):
    print(f"{sys_:22} {d:5} {name:36} {kind:15} {score:4.2f}   {gaps}")
gaps = sum(len(s.gaps()) for s in S)
print(f"\nsurfaces {len(S)}; open facts {gaps}; surfaces with no named owner "
      f"{sum(1 for s in S if not s.owner)}; with no failure contact {sum(1 for s in S if not s.failure_contact)}")
for system, d in [("caldwell claims-core", "write"), ("pennant tms", "read"), ("greystone ehr", "write")]:
    b = best_path(S, system, d)
    print(f"best {d:5} path into {system:20}: {b.name} ({b.score():.2f})")

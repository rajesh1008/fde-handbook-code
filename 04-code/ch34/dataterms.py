"""Listing 34.8: where the data goes, hop by hop, against the clauses that cover each hop."""
import _paths  # noqa: F401

# hop, data, where, retention, clause that covers it (None = nobody's paper covers it yet)
MAPS = {
    "Caldwell (v5, day 149)": [
        ("claim files at rest", "claim documents", "S3 claims-eval, account 111122223333, us-east-1",
         "90 days after the engagement", "CA-15, storage decision day 48"),
        ("runner", "documents and extractions", "role nl-shadow-runner in Caldwell's account", "none (stateless)",
         "CA-15"),
        ("gateway", "prompts and outputs", "Caldwell model gateway (Priya Natarajan)", "Caldwell's gateway logs",
         "CA-15"),
        ("model provider", "prompts and outputs", "provider endpoint behind the gateway",
         "provider terms, dated [VERIFY]", "CA-10 and Exhibit D"),
        ("run records", "versions, inputs, outputs, reviewer", "log group /caldwell/nl-shadow/runner",
         "Caldwell's policy", "CA-07"),
        ("support access", "read-only views", "SSO group nl-shadow-readers (four named)", "session only", "CA-15"),
    ],
    "Greystone (redline, day 108)": [
        ("referrals at rest", "protected health information", "Greystone tenant", "Greystone's policy", "GA-06"),
        ("drafting service", "referral text, drafts", "Greystone tenant", "none (stateless)", "GA-06"),
        ("model provider", "prompts and outputs", "provider endpoint", "provider terms [VERIFY]", "GA-02"),
        ("provider abuse monitoring", "prompts flagged for review", "provider's monitoring store",
         "provider-defined window", None),
    ],
    "Pennant (DPA draft)": [
        ("EU shipment records", "names, addresses of consignees", "europe-west4", "Pennant's policy", "PA-01"),
        ("matching service", "shipment and invoice lines", "europe-west4", "none (stateless)", "PA-01"),
        ("on-call support", "read access during incidents", "engineers outside the EEA", "session only", None),
    ],
}


def main():
    for name, hops in MAPS.items():
        uncovered = [h for h in hops if h[4] is None]
        print(f"DATA MAP  {name}: {len(hops)} hops, {len(hops) - len(uncovered)} covered, {len(uncovered)} uncovered")
        for hop, data, where, ret, cl in hops:
            print(f"  {'UNCOVERED' if cl is None else 'covered  '}  {hop:26} {data:36} {where:48} {ret:30} "
                  f"{cl or '-'}")
        print()
    print("Greystone's uncovered hop is finding F-10 (owner Marcus Bell, due day 120); Pennant's needs a transfer "
          "mechanism in the DPA [VERIFY].")


if __name__ == "__main__":
    main()

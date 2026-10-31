"""The incidents that appear after six months: four timelines on one clock (minutes from day 0), measured with
fieldkit.liveops.Incident. Deterministic stand-in; event times are the lab's."""
import _paths  # noqa: F401
from fieldkit.liveops import Incident
from world import month_of


def t(day, h, m=0):
    return day * 1440 + h * 60 + m


def build():
    out = []
    i = Incident("INC-C-014 Caldwell storm surge, review band overflows")
    i.log(t(428, 8), "start", "volume 2.3x after a severe storm; review band queue grows 310 an hour, clears 140")
    i.log(t(429, 9), "note", "drift monitor: PSI on loss type 0.31, read by Anne Kessler; accuracy line quiet")
    i.log(t(430, 10), "detect", "adjuster leads report review items older than 48 hours; no queue-age alert existed")
    i.log(t(430, 10, 25), "ack", "Anne Kessler opens the incident; Northlight retainer on the bridge")
    i.log(t(430, 16), "mitigate", "eleven adjusters borrowed; queue ordered by age and claim value; router unchanged")
    i.log(t(433, 12), "note", "queue under 24 hours; queue-age page at 24 h and surge mode added to the mode table")
    out.append(("Caldwell", i))
    i = Incident("INC-P-071 Pennant EU lane client certificate expires")
    i.log(t(467, 2, 10), "start", "EU lane mutual TLS fails; documents fail closed to the retry queue")
    i.log(t(467, 2, 16), "detect", "error-rate page to the managed-service night on-call")
    i.log(t(467, 2, 21), "ack", "Northlight night on-call acknowledges; certificate issued day 102, 365 days")
    i.log(t(467, 2, 40), "note", "no US fallback: EU documents stay in the EU lane (DPA); queue holds")
    i.log(t(467, 7, 40), "note", "Nadia Brooks issues a new certificate through Pennant's PKI")
    i.log(t(467, 7, 52), "mitigate", "lane healthy; 412 queued documents processed by 08:30")
    out.append(("Pennant", i))
    i = Incident("INC-G-009 Greystone drafts cite superseded payer criteria")
    i.log(t(384, 0), "start", "largest payer's criteria revision takes effect; the criteria table still holds the old set")
    i.log(t(395, 14), "detect", "Tess Moreno's monthly sample: 9 of 120 drafts with a material error, 6 cite old criteria")
    i.log(t(395, 14, 30), "ack", "Michael Hart and Callum Reid open the incident")
    i.log(t(395, 17, 30), "mitigate", "drafts for the affected service lines withheld; coordinators draft by hand")
    i.log(t(399, 12), "note", "revised table reviewed by Michael Hart; drafts resume; criteria owner added to register")
    out.append(("Greystone", i))
    i = Incident("INC-G-011 Greystone change freeze blocks a critical parser fix (v1)")
    i.log(t(443, 9, 10), "start", "critical advisory for the attachment parser, inside the EHR upgrade freeze")
    i.log(t(443, 9, 10), "detect", "morning conflict check: due day 457, normal path day 466")
    i.log(t(443, 9, 30), "ack", "Callum Reid pages Sam Oakley and the provider change manager")
    i.log(t(443, 11, 40), "mitigate", "mode M3: fax attachments to manual intake")
    i.log(t(446, 2), "note", "emergency change live; mode M3 off at 07:00")
    out.append(("Greystone", i))
    return out


def main():
    print("INCIDENTS AFTER MONTH SIX  (deterministic stand-in)")
    print(f"  {'incident':<62}{'month':>6}{'detect':>10}{'ack':>8}{'mitigate':>10}")
    rows = []
    for c, i in build():
        m = i.metrics(); day = i.first("start") // 1440
        rows.append((c, i.name, month_of(c, day), m))
        print(f"  {i.name:<62}{month_of(c, day):>6}{m['ttd'] / 60:>9.1f}h{m['tta']:>6}m{m['ttm'] / 60:>9.1f}h")
    print("  detect and mitigate are hours from start; ack is minutes from detect")
    print("  what detected each: a person reading a queue (C), a page (P), the customer's monthly sample (G-009),"
          " the conflict check (G-011)")
    return rows


if __name__ == "__main__":
    main()

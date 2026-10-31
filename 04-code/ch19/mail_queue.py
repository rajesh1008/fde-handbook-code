"""Listing 19.3: Caldwell's intake mailbox as a queue. 88 sample messages; the connector crashes after the
durable write and before the acknowledge on 6 of them, so the server redelivers those 6; brokers forward 9
messages a second time with a new Message-ID. Three readers compared. Deterministic stand-in."""
import hashlib
import _paths  # noqa: F401
from fieldkit.connectors import Message, MailQueue
from sim import caldwell_sample

mail = [d for d in caldwell_sample() if d["channel"] == "mail"]
msgs = [Message(f"<{d['doc'].lower()}@broker.example>", "broker@example.com", f"FNOL {d['doc']}",
                [(d["doc"] + ".pdf", hashlib.sha256(d["doc"].encode()).digest() * 40)]) for d in mail]
stream = list(msgs)
stream += [msgs[i] for i in (3, 17, 29, 41, 60, 77)]                         # redelivered after a crash
stream += [Message(m.msg_id.replace("@", ".fwd@"), "agency@example.com", "FW: " + m.subject, m.attachments)
           for m in (msgs[i] for i in (5, 11, 23, 34, 47, 52, 66, 70, 85))]  # forwarded again by a broker
print(f"messages in the mailbox stream: {len(stream)} (sample documents: {len(msgs)})")
for label, keys in [("no dedupe", ()), ("Message-ID only", ("msg_id",)), ("Message-ID + attachment hash",
                                                                          ("msg_id", "attachments"))]:
    q = MailQueue(keys)
    for m in stream:
        q.accept(m)
    by = {}
    for _, k in q.duplicates:
        by[k] = by.get(k, 0) + 1
    print(f"{label:30} documents stored {len(q.store):3}  duplicates caught {len(q.duplicates):2} {by or ''}"
          f"  duplicate documents passed on {len(q.store) - len(msgs)}")

"""Pennant Logistics: map at day 28. One person holds four roles."""
from stakeholders import Person, StakeholderMap

DAY28 = StakeholderMap("Pennant", 28, [
    Person("ruiz", "Jenna Ruiz", "VP Operations", ("sponsor", "operator", "approver", "owner"), 27, source="own words"),
    Person("clerks", "Documentation clerks (14)", "Memphis documentation team", ("operator",), 21, source="observed"),
    Person("compliance", "Compliance manager", "Pennant compliance", ("blocker",), 16,
           reasons=("EU personal data on bills of lading", "customs holds need a human reason code"), source="own words"),
])

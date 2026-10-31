"""Chapter 2 margin model: what one engagement earns and costs in its first contract year.

Every number in a Plan is an input someone has to own. Hours are FDE hours on the account, in five
buckets that match how the work actually spends time; the integration tax is the hours spent making
the customer's systems talk to ours, per hour of model work. Nothing here calls a model.
"""
from dataclasses import dataclass, replace
from typing import Optional

HOURS_PER_FTE_MONTH = 140      # FDE hours a full-time engineer books to one account in a month
LOADED_RATE = 150.0            # Northlight's loaded cost per FDE hour, USD (illustrative, see README)
GATES = ("Architecture Review", "Build Complete", "Shadow Exit", "Model-Risk Approval", "Live Stable")


class BillingBasisMismatch(ValueError):
    """Raised when a forecast assumes a billing basis the contract does not have."""


@dataclass(frozen=True)
class Contract:
    customer: str
    acv: float                         # annual subscription value, USD
    billing: str                       # services basis: "fixed" or "tm"
    services_fee: float = 0.0          # fixed-price deployment fee
    bill_rate: float = 0.0             # T&M rate per FDE hour
    tm_cap: Optional[float] = None     # T&M not-to-exceed
    subscription_starts: str = "signature"   # or "production"

    def __post_init__(self):
        if self.billing not in ("fixed", "tm"):
            raise ValueError(f"unknown billing basis {self.billing!r}")
        if self.subscription_starts not in ("signature", "production"):
            raise ValueError(f"unknown subscription start {self.subscription_starts!r}")


@dataclass(frozen=True)
class Plan:
    label: str
    fde_fte: float                     # engineers on the account until production
    discovery_h: float
    access_h: float                    # access, environment, security questionnaire
    model_h: float                     # prompts, retrieval, evaluation harness, the model-facing code
    integration_tax: float             # integration hours per model-work hour
    gates_h: float                     # evidence, reviews, the five gates
    handover_h: float
    wait_months: float = 0.0           # elapsed months blocked on the customer (access, reviews)
    blocked_burn: float = 0.5          # share of a blocked FDE's month that still lands on the account
    sustain_fte: float = 0.5           # engineers after production, to month 12
    run_pilot: float = 3000.0          # model and hosting cost per month before production
    run_prod: float = 9000.0           # per month in production
    cogs_rate: float = 0.10            # product support and platform share of subscription revenue
    never_live: bool = False

    @property
    def integration_h(self) -> float:
        return self.model_h * self.integration_tax

    @property
    def work_h(self) -> float:
        return self.discovery_h + self.access_h + self.model_h + self.integration_h + self.gates_h + self.handover_h

    @property
    def months_to_production(self) -> float:
        return self.work_h / (self.fde_fte * HOURS_PER_FTE_MONTH) + self.wait_months

    @property
    def blocked_h(self) -> float:
        return self.wait_months * self.fde_fte * HOURS_PER_FTE_MONTH * self.blocked_burn


@dataclass
class YearOne:
    customer: str
    plan: str
    billing_assumed: str
    months_to_production: Optional[float]
    hours: float
    subscription: float
    services: float
    fde_cost: float
    run_cost: float
    cogs: float

    @property
    def revenue(self) -> float:
        return self.subscription + self.services

    @property
    def cost(self) -> float:
        return self.fde_cost + self.run_cost + self.cogs

    @property
    def margin(self) -> float:
        return (self.revenue - self.cost) / self.revenue if self.revenue else float("-inf")


def check_billing_basis(contract: Contract, assumed: str) -> None:
    if assumed != contract.billing:
        raise BillingBasisMismatch(
            f"{contract.customer}: forecast assumes {assumed!r} but the contract is {contract.billing!r}")


def year_one(contract: Contract, plan: Plan, assume_billing: Optional[str] = None, strict: bool = True) -> YearOne:
    """Year-one P&L for one engagement. assume_billing lets a forecast (wrongly) override the contract."""
    basis = assume_billing or contract.billing
    if strict:
        check_billing_basis(contract, basis)
    m = None if plan.never_live else min(plan.months_to_production, 12.0)
    live_months = 0.0 if m is None else 12.0 - m
    pre_h = plan.work_h - plan.handover_h if m is None else plan.work_h
    if m is not None and plan.months_to_production > 12:      # only the year-one share of the work
        pre_h *= 12.0 / plan.months_to_production
    blocked = plan.blocked_h if m is None or plan.months_to_production <= 12 else plan.blocked_h * 12.0 / plan.months_to_production
    sustain_h = plan.sustain_fte * HOURS_PER_FTE_MONTH * live_months
    hours = pre_h + blocked + sustain_h
    if contract.subscription_starts == "signature":
        sub = contract.acv
    else:
        sub = contract.acv * live_months / 12.0
    if basis == "fixed":
        services = contract.services_fee
    else:
        rate = contract.bill_rate or 260.0
        billable = pre_h                                      # blocked hours are not billable
        services = billable * rate
        if contract.tm_cap is not None:
            services = min(services, contract.tm_cap)
    pilot_months = 12.0 if m is None else m
    run = plan.run_pilot * pilot_months + plan.run_prod * live_months
    return YearOne(contract.customer, plan.label, basis, m, hours, sub, services,
                   hours * LOADED_RATE, run, sub * plan.cogs_rate)


def pilot_month_cost(contract: Contract, plan: Plan) -> dict:
    """What one more month before production costs: FDE burn, run cost, and deferred subscription."""
    burn_h = plan.fde_fte * HOURS_PER_FTE_MONTH * plan.blocked_burn
    deferred = contract.acv / 12.0 if contract.subscription_starts == "production" else 0.0
    return dict(fde_hours=burn_h, fde_cost=burn_h * LOADED_RATE, run=plan.run_pilot,
                deferred_subscription=deferred, total=burn_h * LOADED_RATE + plan.run_pilot + deferred)


def renewal_probability(months_to_production: Optional[float]) -> float:
    """Northlight's renewal history across its 38 customers, banded by time to production (illustrative)."""
    if months_to_production is None:
        return 0.20
    if months_to_production <= 6:
        return 0.93
    if months_to_production <= 9:
        return 0.80
    return 0.62


def gate_days(plan: Plan) -> dict:
    """Day each of the five gates is planned to pass, spreading the plan's work and waits in order."""
    per_day = plan.fde_fte * HOURS_PER_FTE_MONTH / 30.0
    wait_d = plan.wait_months * 30.0
    t = (plan.discovery_h + plan.access_h) / per_day + 0.5 * wait_d
    out = {"Architecture Review": t}
    t += (plan.model_h + plan.integration_h) / per_day + 0.3 * wait_d
    out["Build Complete"] = t
    t += 0.5 * plan.gates_h / per_day + 0.1 * wait_d
    out["Shadow Exit"] = t
    t += 0.5 * plan.gates_h / per_day + 0.1 * wait_d
    out["Model-Risk Approval"] = t
    t += plan.handover_h / per_day
    out["Live Stable"] = t
    return {k: round(v) for k, v in out.items()}


def with_(plan: Plan, **kw) -> Plan:
    return replace(plan, **kw)


def two_year_gross_profit(contract: Contract, plan: Plan) -> dict:
    """Year-one gross profit plus year two weighted by the renewal band. Year two is a steady account:
    full subscription, sustain engineers all year, production run cost (or pilot run cost if never live)."""
    y1 = year_one(contract, plan)
    p = renewal_probability(None if plan.never_live else plan.months_to_production)
    run = (plan.run_pilot if plan.never_live else plan.run_prod) * 12
    y2_cost = plan.sustain_fte * HOURS_PER_FTE_MONTH * 12 * LOADED_RATE + run + contract.acv * plan.cogs_rate
    y2 = contract.acv - y2_cost
    return dict(year_one=y1.revenue - y1.cost, year_two=y2, renewal=p, total=y1.revenue - y1.cost + p * y2)

"""A deterministic stand-in for Caldwell's AWS team account (no cloud is called).

It reads the same Terraform JSON that Caldwell's pipeline applies, and models only what this chapter needs: which
resources a plan creates, which destinations the runner can reach, and the egress log Caldwell owns."""
import json, pathlib
import _paths  # noqa: F401
from fieldkit.environment import AuditLog, EgressPolicy, EgressRule

HERE = pathlib.Path(__file__).resolve().parent
ACCOUNT, REGION = "111122223333", "us-east-1"          # documentation-style account id
GATEWAY_HOST = "gateway.preprod.caldwell.internal"


def load(name="main.tf.json"):
    return json.loads((HERE / "terraform" / name).read_text())


def plan(tf):
    res = tf["resource"]
    n = sum(len(v) for v in res.values())
    sg = res["aws_security_group"]["runner"]["egress"]
    return dict(add=n, igw=len(res.get("aws_internet_gateway", {})), nat=len(res.get("aws_nat_gateway", {})),
                public_ip=res["aws_ecs_service"]["runner"]["network_configuration"]["assign_public_ip"],
                egress=[f"tcp/{r['from_port']} to {','.join(r['cidr_blocks'])}" for r in sg],
                endpoints=list(res["aws_vpc_endpoint"]))


def egress_policy(tf, log):
    """Only interface or gateway endpoints are reachable: there is no route out of the VPC."""
    owner = "Priya Natarajan (Caldwell)"
    hosts = dict(gateway=(GATEWAY_HOST, "model calls through the gateway"),
                 secretsmanager=(f"secretsmanager.{REGION}.amazonaws.com", "read the gateway key"),
                 logs=(f"logs.{REGION}.amazonaws.com", "runner logs to Caldwell"),
                 s3=(f"caldwell-nl-sandbox-slices.s3.{REGION}.amazonaws.com", "slice in, results out (endpoint policy: this bucket only)"))
    rules = [EgressRule(k, hosts[k][0], owner=owner, reason=hosts[k][1]) for k in tf["resource"]["aws_vpc_endpoint"]]
    return EgressPolicy("nl-shadow-runner", rules, log)


def container_env(tf):
    cd = json.loads(tf["resource"]["aws_ecs_task_definition"]["runner"]["container_definitions"])[0]
    return {e["name"]: e["value"] for e in cd.get("environment", [])}, [s["name"] for s in cd.get("secrets", [])]

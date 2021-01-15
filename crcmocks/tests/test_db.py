from crcmocks.db import upsert_org, get_org


def test_upsert_org():
    upsert_org(org_id="12345", ebs_account="54321", external_id="external_12345")
    found_org = get_org("12345")
    assert found_org.get("org_id") == "12345"
    assert found_org.get("ebs_account") == "54321"
    assert found_org.get("external_id") == "external_12345"


def test_get_org_negative():
    found_org = get_org("non_existent_org")
    assert not found_org

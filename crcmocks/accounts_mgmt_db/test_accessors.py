import uuid
from crcmocks.accounts_mgmt_db.accessors import (
    upsert_org,
    get_org_by_id,
    insert_account_mapping,
    get_account_by_id,
)


# This source file contains unit tests of the functions provided in
# crcmocks.accounts_mgmt_db.accessors.


def test_upsert_org():
    """
    Happy path test of upserting an org.
    """
    upsert_org(org_id="12345", ebs_account="54321", external_id="external_12345")
    found_org = get_org_by_id("12345")
    assert found_org.get("org_id") == "12345"
    assert found_org.get("ebs_account") == "54321"
    assert found_org.get("external_id") == "external_12345"


def test_get_org_negative():
    """
    Try to find a non-existent org, confirm result is None.
    """
    found_org = get_org_by_id("non_existent_org")
    assert not found_org


def test_get_account_by_id():
    """ Happy path, retrieve an existing account. """
    upsert_org("12345", "54321", "external3222")
    insert_account_mapping("new_account_12345", "12345")

    result = get_account_by_id("new_account_12345")
    assert len(result) == 1
    assert result[0].get("org_id") == "12345"


def test_get_account_by_id_negative():
    pass


def test_upsert_account():
    unique_org = uuid.uuid4()
    org_id = f"fake_org{unique_org}"
    ebs_account_id = f"fake_ebs{unique_org}"
    external_id = f"fake_external{unique_org}"
    upsert_org(org_id, ebs_account_id, external_id)
    fake_account = f"fake_account{unique_org}"
    insert_account_mapping(fake_account, org_id)
    result = get_account_by_id(fake_account)
    assert len(result) == 1
    assert result[0].get("org_id") == org_id

    second_org = uuid.uuid4()
    second_org_id = f"fake_org{second_org}"
    second_ebs_account_id = f"fake_ebs{second_org}"
    second_external_id = f"fake_external{second_org}"
    upsert_org(second_org_id, second_ebs_account_id, second_external_id)
    insert_account_mapping(fake_account, second_org_id)
    result = get_account_by_id(fake_account)
    assert len(result) == 2


def test_upsert_account_negative():
    pass

from pathlib import Path
import pytest
from gltest import get_contract_factory
from gltest.assertions import tx_execution_succeeded
from gltest.types import TransactionStatus
from gltest.utils import extract_contract_address

ARGS = ["Will export preserve formulas, formatting, and hidden worksheet state?", "The answer must separately state what happens to formulas, formatting, and hidden worksheets."]

@pytest.mark.integration
def test_studionet_two_party_answer(default_account, secondary_account):
    factory = get_contract_factory(contract_file_path=Path(__file__).resolve().parents[2] / "contracts" / "did_they_answer.py")
    deployed = factory.deploy_contract_tx(args=ARGS, account=default_account, wait_transaction_status=TransactionStatus.FINALIZED)
    assert tx_execution_succeeded(deployed)
    address = extract_contract_address(deployed)
    respondent = factory.build_contract(address, account=secondary_account)
    submitted = respondent.submit_answer(args=["Formulas and formatting are preserved, while hidden worksheet state is not yet supported."]).transact(wait_transaction_status=TransactionStatus.FINALIZED)
    assert tx_execution_succeeded(submitted)
    reviewed = respondent.review_answer(args=[]).transact(wait_transaction_status=TransactionStatus.FINALIZED)
    assert tx_execution_succeeded(reviewed)
    case = respondent.get_case(args=[]).call()
    assert case["verdict"] in ("ANSWERED", "PARTIAL", "EVADED")
    assert case["respondent"] == str(secondary_account.address).lower()
    print(f"STUDIONET_ADDRESS={address}")
    print(f"STUDIONET_DEPLOY_TX={deployed['hash']}")
    print(f"STUDIONET_WRITE_TX={reviewed['hash']}")
    print(f"STUDIONET_RESULT={case['verdict']}")


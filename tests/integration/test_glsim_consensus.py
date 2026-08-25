from __future__ import annotations
import json
from pathlib import Path
from gltest import get_contract_factory, get_validator_factory
from gltest.accounts import create_accounts
from gltest.assertions import tx_execution_succeeded
from gltest.types import TransactionStatus
from gltest.utils import extract_contract_address

PROMPT = "independently determine whether"
ARGS = ["Will export preserve formulas, formatting, and hidden worksheet state?", "The answer must separately state what happens to formulas, formatting, and hidden worksheets."]

def context():
    validators = get_validator_factory().batch_create_mock_validators(5, mock_llm_response={"nondet_exec_prompt": {PROMPT: json.dumps({"verdict": "ANSWERED"})}})
    return {"validators": [v.to_dict() for v in validators]}

def test_five_validator_two_party_answer():
    asker, respondent = create_accounts(2)
    factory = get_contract_factory(contract_file_path=Path(__file__).resolve().parents[2] / "contracts" / "did_they_answer.py")
    deployed = factory.deploy_contract_tx(args=ARGS, account=asker, wait_transaction_status=TransactionStatus.FINALIZED)
    assert tx_execution_succeeded(deployed)
    contract = factory.build_contract(extract_contract_address(deployed), account=respondent)
    submitted = contract.submit_answer(args=["Formulas and formatting are preserved, while hidden worksheet state is not yet supported."]).transact(wait_transaction_status=TransactionStatus.FINALIZED)
    assert tx_execution_succeeded(submitted)
    reviewed = contract.review_answer(args=[]).transact(transaction_context=context(), wait_transaction_status=TransactionStatus.FINALIZED)
    assert tx_execution_succeeded(reviewed)
    assert contract.get_case(args=[]).call()["phase"] == "FINAL"


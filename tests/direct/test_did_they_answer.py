from pathlib import Path
import json

CONTRACT = Path(__file__).resolve().parents[2] / "contracts" / "did_they_answer.py"
SDK = "v0.2.16"
PROMPT = "independently determine whether"
ARGS = (
    "Will the export feature preserve formulas, formatting, and hidden worksheet state?",
    "An answer must separately state what happens to formulas, cell formatting, and hidden worksheets.",
)


def deploy(vm, direct_deploy, alice):
    vm.sender = alice
    return direct_deploy(str(CONTRACT), *ARGS, sdk_version=SDK)


def test_answer_challenge_and_final_consensus(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = deploy(direct_vm, direct_deploy, direct_alice)
    direct_vm.sender = direct_bob
    contract.submit_answer("Formulas and formatting are preserved. Hidden worksheet state is not yet supported.")
    direct_vm.mock_llm(PROMPT, json.dumps({"verdict": "PARTIAL"}))
    contract.review_answer()
    assert contract.get_case()["phase"] == "CHALLENGE_OPEN"
    direct_vm.sender = direct_alice
    contract.challenge_verdict("The response explicitly covers all three requested points, including the unsupported hidden state.")
    direct_vm.clear_mocks()
    direct_vm.mock_llm(PROMPT, json.dumps({"verdict": "ANSWERED"}))
    contract.review_answer()
    assert contract.get_case()["phase"] == "FINAL"
    assert contract.get_case()["resolution"] == "CONSENSUS"
    leader = direct_vm._captured_validators[-1][0]
    assert direct_vm.run_validator(leader_result=leader) is True


def test_asker_cannot_self_answer_and_only_asker_challenges(direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie):
    contract = deploy(direct_vm, direct_deploy, direct_alice)
    with direct_vm.expect_revert("asker_cannot_answer"):
        contract.submit_answer("This self-answer should not be accepted even though it has sufficient length.")
    direct_vm.sender = direct_bob
    contract.submit_answer("Formulas are preserved, but this response does not address formatting or hidden worksheets.")
    direct_vm.mock_llm(PROMPT, json.dumps({"verdict": "EVADED"}))
    contract.review_answer()
    direct_vm.sender = direct_charlie
    with direct_vm.expect_revert("only_asker"):
        contract.challenge_verdict("An unrelated account must not be able to control the challenge path.")


def test_invalid_verdict_fails_closed(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = deploy(direct_vm, direct_deploy, direct_alice)
    direct_vm.sender = direct_bob
    contract.submit_answer("Formulas and formatting are preserved, and hidden worksheets stay hidden after export.")
    direct_vm.mock_llm(PROMPT, json.dumps({"verdict": "MAYBE"}))
    with direct_vm.expect_revert("invalid_verdict"):
        contract.review_answer()
    assert contract.get_case()["phase"] == "READY_FOR_REVIEW"


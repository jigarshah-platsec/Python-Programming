"""
Day 4: (The "IAM Policy Engine")
Security is defined by Policies. A policy isn't just a list; it's a Tree of logic.
"Allow if (Admin AND MFA) OR (Breakglass)"

The "Staff" Level Trap:
A Junior engineer writes 50 if/else statements.
A Staff engineer writes a recursive evaluator that can handle infinite nesting.

Practice Problem: The Recursive Policy Evaluator
Scenario:
You need to write a function is_authorized(policy, user_attributes) that returns True or False.

Input:
policy: A nested dictionary representing logic gates (AND, OR) or a specific string requirement (leaf node).
Example Policy:
Python
policy = {
    "OR": [
        {"AND": ["role:admin", "mfa:true"]},  # Rule 1: Admin with MFA
        "role:breakglass"                     # Rule 2: OR just Breakglass
    ]
}
user_attributes: A set of strings possessed by the user.
Example: {"sub:jigar", "role:engineer", "mfa:true"}

Task:
Write is_authorized(policy, user_attributes).

Hint:

Base Case: If policy is a string, check if it exists in user_attributes.

Recursive Step:

If policy is a dict with key "OR", return any(...) of the children.

If policy is a dict with key "AND", return all(...) of the children.
"""
from typing import Dict, List

def evaluate_policy(policy: Dict[str, List], user_attributes: List[str]) -> bool:
    """
    Recursively evaluates a boolean policy against user attributes.
    """
    # 1. Base Case: Leaf Node (String)
    if isinstance(policy, str):
        return policy in user_attributes

    # 2. Recursive Step: AND Logic
    if "AND" in policy:
        # Generator expression: Short-circuits if ANY child is False
        return all(evaluate_policy(child, user_attributes) for child in policy["AND"])

    # 3. Recursive Step: OR Logic
    if "OR" in policy:
        # Generator expression: Short-circuits if ANY child is True
        return any(evaluate_policy(child, user_attributes) for child in policy["OR"])

    # 4. Fallback (Invalid Policy Structure)
    return False


def main():
    policy = {
    "OR": [
        {"AND": ["role:admin", "mfa:true"]},  # Rule 1: Admin with MFA
        "role:breakglass"                     # Rule 2: OR just Breakglass
    ]
    }
    user_attributes = ["sub:jigar", "role:engineer", "mfa:true"]
    result = evaluate_policy(policy, user_attributes)
    assert result == False
    user_attributes = ["sub:jigar", "role:admin", "mfa:false"]
    result = evaluate_policy(policy, user_attributes)
    assert result == False
    user_attributes = ["sub:jigar", "role:admin", "mfa:true"]
    result = evaluate_policy(policy, user_attributes)
    assert result == True           # Because of admin+mfa
    user_attributes = ["sub:jigar", "role:breakglass", "mfa:false"]
    result = evaluate_policy(policy, user_attributes)
    assert result == True           # Because of breakglass


if "__name__" == "__main__":
    main()
"""
Plaid: routing number → bank ID
================================
Pattern: Invert → Join → Vote

  name_to_bank_id is many-to-many (aliases AND collisions).
  Invert once:  name → set(ids)
  Join:         rn → name → [ids]
  Vote (Part 2): providers disagree on names; aliases like
                 "Wells" / "Wells Fargo" are the SAME id, so
                 count votes on ids, not names. Keep all max-vote ids.

Complexity
  invert     O(N)
  Part 1     O(R)
  Part 2     O(P * R * K)   K = ids per name, tiny
"""

from collections import defaultdict, Counter


def invert_names(name_to_bank_id):
    """Edge list → lookup. Dedup ids per name."""
    name_to_ids = defaultdict(set)
    for name, bank_id in name_to_bank_id:
        name_to_ids[name].add(bank_id)
    return name_to_ids


# --- Part 1: one provider -----------------------------------------------

def create_routing_number_mapping(rn_to_name, name_to_bank_id):
    name_to_ids = invert_names(name_to_bank_id)
    return {
        rn: sorted(name_to_ids[name])   # missing name → []
        for rn, name in rn_to_name.items()
    }


# --- Part 2: many providers, best guess ---------------------------------

def best_guess_mapping(rn_to_name_list, name_to_bank_id):
    name_to_ids = invert_names(name_to_bank_id)
    votes = defaultdict(Counter)        # rn → Counter(bank_id → count)

    for provider in rn_to_name_list:
        for rn, name in provider.items():
            for bank_id in name_to_ids[name]:
                votes[rn][bank_id] += 1

    result = {}
    for rn, counts in votes.items():
        top = max(counts.values())
        result[rn] = sorted(bid for bid, c in counts.items() if c == top)
    return result


# --- data ----------------------------------------------------------------

name_to_bank_id = [
    ("Wells Fargo", 1),
    ("Wells", 1),
    ("Chase", 2),
    ("Capital One", 3),
    ("Bank of America", 4),
    ("First State Bank", 5),
    ("First State Bank", 6),
]

rn_to_name = {
    "123": "Wells Fargo",
    "456": "Chase",
    "789": "Capital One",
    "555": "First State Bank",
}

rn_to_name_list = [
    {
        "123": "Wells Fargo",
        "456": "Chase",
        "555": "First State Bank",
        "556": "First State Bank",
    },
    {
        "123": "Wells",
        "789": "Capital One",
        "456": "Bank of America",
        "555": "Bank of America",
        "556": "First State Bank",
    },
    {
        "123": "Bank of America",
        "456": "Chase",
    },
]


# --- Part 1 --------------------------------------------------------------
got = create_routing_number_mapping(rn_to_name, name_to_bank_id)
assert got == {
    "123": [1],
    "456": [2],
    "789": [3],
    "555": [5, 6],          # one name, two banks — keep both
}

# --- Part 2 --------------------------------------------------------------
# 123: Wells Fargo→1, Wells→1, BoA→4          → 1 wins (aliases combine)
# 456: Chase→2, BoA→4, Chase→2                → 2 wins
# 555: FSB→5,6  BoA→4                         → three-way tie
# 556: FSB, FSB                               → [5, 6] agreed name, still two banks
# 789: Capital One→3                          → [3]
got = best_guess_mapping(rn_to_name_list, name_to_bank_id)
assert got == {
    "123": [1],
    "456": [2],
    "555": [4, 5, 6],
    "556": [5, 6],
    "789": [3],
}

print("ok")

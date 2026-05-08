"""
MarketPlace: Quotes for Assets
Dealer: 
-- puts a quote (user, asset, buy_price, sell_price)    -- Make quote available to market
-- views a quote (user, asset)                          --- Shows a random quote from all available quotes
-- executes a quote (user, asset, buy_price, sell_price)--- Removes given quote from market

Constant Streaminig of Quotes
"""
from random import randint
from typing import List, Set
from collections import defaultdict
class MarketPlace:
    def __init__(self):
        self.quotes = defaultdict(list)

    def add_quote(self, user, asset, buy_price, sell_price) -> bool:
        self.quotes[asset].append([user, buy_price, sell_price])
        return True
    
    def view_quote(self, excluded_user, asset): 
        # If asset is not available in MarketPlace or has no quotes
        if asset not in self.quotes or not self.quotes[asset]:
            return None
        
        valid_indices = []
        for index, quote in enumerate(self.quotes[asset]):
            current_user = quote[0]
            if current_user != excluded_user:
                valid_indices.append(index)
        
        if not valid_indices:
            return None
            
        # randint is inclusive, so we must subtract 1 from length
        random_choice_idx = randint(0, len(valid_indices) - 1)
        return valid_indices[random_choice_idx]

    def execute_quote(self, user, asset, quoteIndex) -> bool:
        if quoteIndex is None:
            return False
        
        # Remove this quote for the asset
        self.quotes[asset].pop(quoteIndex)

        # Remove this asset, if all quotes are gone!
        if not len(self.quotes[asset]):
            del self.quotes[asset]

        return True
    

def main():
    marketPlace = MarketPlace()
    assert marketPlace.add_quote("Jigar", "APPLE", 10, 20) == True
    assert marketPlace.view_quote("Jigar", "APPLE") == None   # No quotes shown because quotes available only belongs to "Jigar" already
    assert marketPlace.add_quote("Jigar", "APPLE", 10, 20) == True
    
    resQuoteIndex = marketPlace.view_quote("Krupa", "APPLE")    # Random quote returned
    assert resQuoteIndex in [0, 1]
    assert marketPlace.execute_quote("Krupa", "APPLE", resQuoteIndex) == True

    assert marketPlace.execute_quote("Krupa", "APPLE", None) == False


    print(marketPlace.quotes)
    resQuoteIndex = marketPlace.view_quote("Krupa", "APPLE")    # Random quote returned
    print(resQuoteIndex)
    assert resQuoteIndex in [0]
    assert marketPlace.execute_quote("Krupa", "APPLE", resQuoteIndex) == True
    
if __name__ == "__main__":
    main()


""" Optimized for view_quotes() using "USER" as one of the Dict Key """
from random import choice, randint
from collections import defaultdict

class MarketPlace:
    def __init__(self):
        # Data Structure: 
        # { asset: { user: [ [buy, sell], [buy, sell] ... ] } }
        self.quotes = defaultdict(lambda: defaultdict(list))
        
        # Fast User Lookup: 
        # { asset: [user1, user2, ...] }
        self.asset_users = defaultdict(list)
        
        # Helper map to remove users in O(1)
        # { asset: { user: index_in_asset_users_list } }
        self.user_indices = defaultdict(dict)

    def add_quote(self, user, asset, buy_price, sell_price) -> bool:
        # 1. Add user to the "Active Users" list if new for this asset
        if user not in self.quotes[asset]:
            self.user_indices[asset][user] = len(self.asset_users[asset])
            self.asset_users[asset].append(user)
            
        # 2. Add the quote to that user's specific bucket
        self.quotes[asset][user].append([buy_price, sell_price])
        return True
    
    def view_quote(self, viewer, asset):
        # Safety Check
        if asset not in self.asset_users or not self.asset_users[asset]:
            return None

        users_list = self.asset_users[asset]
        num_users = len(users_list)

        # Edge Case: Only the viewer has quotes
        if num_users == 1 and users_list[0] == viewer:
            return None

        # --- STEP 1: Pick a Target User O(1) ---
        rand_idx = randint(0, num_users - 1)
        target_user = users_list[rand_idx]

        # If we accidentally picked the viewer, just step forward by one!
        # This is deterministic O(1) - no while loops.
        if target_user == viewer:
            rand_idx = (rand_idx + 1) % num_users
            target_user = users_list[rand_idx]

        # --- STEP 2: Pick a Random Quote from Target User O(1) ---
        user_quotes = self.quotes[asset][target_user]
        quote_idx = randint(0, len(user_quotes) - 1)
        
        # Return a "Handle" composed of (Owner, Index) so we can execute it later
        return (target_user, quote_idx)

    def execute_quote(self, viewer, asset, quote_handle) -> bool:
        if not quote_handle or asset not in self.quotes:
            return False

        owner, idx = quote_handle
        user_quotes = self.quotes[asset][owner]

        # Safety: Index out of bounds check
        if idx < 0 or idx >= len(user_quotes):
            return False

        # --- STEP 3: Remove Quote O(1) using Swap-and-Pop ---
        last_quote = user_quotes[-1]
        user_quotes[idx] = last_quote
        user_quotes.pop()

        # --- Cleanup: If user has no more quotes, remove user from list O(1) ---
        if not user_quotes:
            del self.quotes[asset][owner]
            
            # Remove owner from asset_users list in O(1)
            user_idx_in_list = self.user_indices[asset][owner]
            last_user = self.asset_users[asset][-1]
            
            # Swap current user with last user
            self.asset_users[asset][user_idx_in_list] = last_user
            self.user_indices[asset][last_user] = user_idx_in_list
            
            # Pop last user
            self.asset_users[asset].pop()
            del self.user_indices[asset][owner]

            # Cleanup asset if empty
            if not self.asset_users[asset]:
                del self.asset_users[asset]
                del self.user_indices[asset]

        return True

def main():
    m = MarketPlace()
    m.add_quote("Jigar", "APPL", 100, 101) # Jigar Index 0
    m.add_quote("Jigar", "APPL", 102, 103) # Jigar Index 1
    m.add_quote("Alice", "APPL", 200, 201) # Alice Index 0

    # Test 1: Jigar should ALWAYS see Alice
    handle = m.view_quote("Jigar", "APPL")
    assert handle == ("Alice", 0) 
    print("Test 1 Passed: Jigar saw Alice immediately.")

    # Test 2: Alice should ALWAYS see Jigar (one of them)
    handle = m.view_quote("Alice", "APPL")
    assert handle[0] == "Jigar"
    print(f"Test 2 Passed: Alice saw Jigar's quote index {handle[1]}")

    # Test 3: Execute Alice's quote
    # Note: We pass the HANDLE returned by view_quote
    m.execute_quote("Jigar", "APPL", ("Alice", 0))
    
    # Test 4: Jigar tries to view again -> Should be None (Alice is empty)
    assert m.view_quote("Jigar", "APPL") is None
    print("Test 4 Passed: No more quotes for Jigar to see.")

if __name__ == "__main__":
    main()
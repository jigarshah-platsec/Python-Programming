import unittest
from http_parser import find_leaked_emails

class DummyApiClient:
    """A fake API client to simulate pagination and agent configs."""
    def __init__(self, pages):
        self.pages = pages
        
    def get_configs(self, page_token=None):
        if page_token == "token_page_2":
            return self.pages[1]
        elif page_token == "token_page_3":
            return self.pages[2]
        
        # Default to first page
        return self.pages[0]

class TestHttpParser(unittest.TestCase):
    def test_find_leaked_emails_single_page(self):
        mock_data = [
            {
                "next_page_token": None,
                "agents": [
                    {"agent_id": "agent_1", "context_window": "Hello user, please contact admin@company.com for help."},
                    {"agent_id": "agent_2", "context_window": "This is a clean prompt! No emails here."},
                    {"agent_id": "agent_3", "context_window": "Also clean."}
                ]
            }
        ]
        client = DummyApiClient(mock_data)
        vulnerable_agents = find_leaked_emails(client)
        
        # The user's code returns a list of unique items, let's sort to match
        self.assertEqual(sorted(vulnerable_agents), ["agent_1"])

    def test_find_leaked_emails_pagination(self):
        mock_data = [
            {
                "next_page_token": "token_page_2",
                "agents": [
                    {"agent_id": "agent_1", "context_window": "Prompt without emails."},
                    {"agent_id": "agent_2", "context_window": "Send info to user123@gmail.com immediately."}
                ]
            },
            {
                "next_page_token": "token_page_3",
                "agents": [
                    {"agent_id": "agent_3", "context_window": "Clean prompt"},
                    {"agent_id": "agent_4", "context_window": "Please cc support@sierra.ai and help@sierra.ai"}
                ]
            },
            {
                "next_page_token": None,
                "agents": [
                    {"agent_id": "agent_5", "context_window": "Another clean prompt."}
                ]
            }
        ]
        
        client = DummyApiClient(mock_data)
        vulnerable_agents = find_leaked_emails(client)
        
        # agent_2 and agent_4 both have emails in their context windows
        self.assertEqual(set(vulnerable_agents), {"agent_2", "agent_4"})

    def test_find_leaked_emails_no_leaks(self):
        mock_data = [
            {
                "next_page_token": None,
                "agents": [
                    {"agent_id": "agent_x", "context_window": "Just some instructions. email should be here but isn't."},
                    {"agent_id": "agent_y", "context_window": "admin@company is not a valid email"}  # Testing bad email formats
                ]
            }
        ]
        client = DummyApiClient(mock_data)
        vulnerable_agents = find_leaked_emails(client)
        
        self.assertEqual(vulnerable_agents, [])

if __name__ == '__main__':
    unittest.main()

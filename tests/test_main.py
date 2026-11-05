import unittest

from main import (
    get_state,
    get_valid_actions,
    calculate_reward,
    SERVERS,
)


class TestSmartDeploy(unittest.TestCase):

    def test_low_workload(self):
        self.assertEqual(get_state(200), "Low")

    def test_medium_workload(self):
        self.assertEqual(get_state(500), "Medium")

    def test_high_workload(self):
        self.assertEqual(get_state(900), "High")

    def test_valid_actions(self):
        self.assertEqual(get_valid_actions(200), [0, 1, 2])
        self.assertEqual(get_valid_actions(500), [1, 2])
        self.assertEqual(get_valid_actions(900), [2])

    def test_overloaded_server_reward(self):
        reward = calculate_reward(500, SERVERS[0])
        self.assertEqual(reward, -100)

    def test_successful_deployment_reward(self):
        reward = calculate_reward(100, SERVERS[0])
        self.assertAlmostEqual(reward, 10 + (100 / 300 * 5) - 2)


if __name__ == "__main__":
    unittest.main()
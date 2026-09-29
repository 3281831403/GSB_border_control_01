import unittest

import core


class TestCore(unittest.TestCase):
    def test_01_no_duplicate_declare(self):
        state = core.new_game()
        self.assertTrue(core.declare(state, "G1"))
        self.assertFalse(core.declare(state, "G1"))

    def test_02_lane_capacity(self):
        state = core.new_game()
        core.receive(state, "G1")
        core.receive(state, "G2")
        result = core.receive(state, "G3")
        self.assertFalse(result)

    def test_03_fee_exact(self):
        state = core.new_game()
        self.assertEqual(core.fee(state, "G1", 3), 2)

    def test_04_cancel_refunds(self):
        state = core.new_game()
        state["credit"] = 80
        core.cancel(state, "G1")
        self.assertEqual(state["credit"], 100)

    def test_05_no_assign_absent_officer(self):
        state = core.new_game()
        core.declare(state, "G1")
        result = core.assign(state, "G1", "O2")
        self.assertFalse(result)

    def test_06_inspect_fail_no_cost(self):
        state = core.new_game()
        core.declare(state, "G1")
        state["goods"]["G1"]["failed"] = True
        before = state["credit"]
        result = core.inspect(state, "G1")
        self.assertFalse(result)
        self.assertEqual(state["credit"], before)

    def test_07_violation_once(self):
        state = core.new_game()
        core.violation(state)
        self.assertEqual(state["credit"], 90)

    def test_08_load_preserves_decl(self):
        state = core.new_game()
        state["decl_id"] = 4
        loaded = core.load_state(core.save_state(state))
        self.assertEqual(loaded["decl_id"], 4)


if __name__ == "__main__":
    unittest.main()

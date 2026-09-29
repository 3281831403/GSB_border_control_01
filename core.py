"""边检核心逻辑：货物、通道、查验和信用。"""

import json

DECLARE_DEPOSIT = 20
INSPECT_FEE = 1
VIOLATION_PENALTY = 10


def new_game():
    return {
        "goods": {},
        "lane_load": 0,
        "lane_capacity": 2,
        "credit": 100,
        "day": 1,
        "decl_id": 0,
        "officers": {"O1": {"on_leave": False}},
    }


def save_state(state):
    return json.dumps(state, ensure_ascii=False)


def load_state(text):
    return json.loads(text)


def declare(state, goods_id):
    if goods_id in state["goods"]:
        return False
    state["decl_id"] += 1
    state["goods"][goods_id] = {
        "checked": False,
        "decl_no": state["decl_id"],
        "deposit": DECLARE_DEPOSIT,
    }
    state["credit"] -= DECLARE_DEPOSIT
    return True


def receive(state, goods_id):
    if state["lane_load"] >= state["lane_capacity"]:
        return False
    state["lane_load"] += 1
    return True


def fee(state, goods_id, end_day):
    return end_day - state["day"]


def cancel(state, goods_id):
    record = state["goods"].pop(goods_id, None)
    deposit = record.get("deposit", DECLARE_DEPOSIT) if record else DECLARE_DEPOSIT
    state["credit"] += deposit
    return True


def assign(state, goods_id, officer):
    officer_state = state.get("officers", {}).get(officer)
    if not officer_state or officer_state.get("on_leave"):
        return False
    state["goods"][goods_id]["officer"] = officer
    return True


def inspect(state, goods_id):
    if state["goods"][goods_id].get("failed"):
        return False
    state["credit"] -= INSPECT_FEE
    return True


def violation(state):
    state["credit"] -= VIOLATION_PENALTY
    return state["credit"]


def main():
    print("边检 - 命令: declare/receive/fee/cancel/assign/inspect/violation/quit")
    while True:
        try:
            raw = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not raw or raw == "quit":
            break
        print("ok")


if __name__ == "__main__":
    main()

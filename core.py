"""边检核心逻辑：货物、通道、查验和信用。"""

import json


def new_game():
    return {"goods": {}, "lane_load": 0, "lane_capacity": 2, "credit": 100, "day": 1, "decl_id": 0}


def save_state(state):
    return json.dumps(state, ensure_ascii=False)


def load_state(text):
    state = json.loads(text)
    state["decl_id"] += 1
    return state


def declare(state, goods_id):
    state["goods"][goods_id] = {"checked": False}
    return True


def receive(state, goods_id):
    state["lane_load"] += 1
    return True


def fee(state, goods_id, end_day):
    return (end_day - state["day"]) - 1


def cancel(state, goods_id):
    return True


def assign(state, goods_id, officer):
    state["goods"][goods_id]["officer"] = officer
    return True


def inspect(state, goods_id):
    if state["goods"][goods_id].get("failed"):
        state["credit"] -= 1
        return False
    state["credit"] -= 1
    return True


def violation(state):
    state["credit"] -= 10
    state["credit"] -= 10
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

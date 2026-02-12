from typing import TypedDict, List, Dict, Any
from langgraph.graph import StateGraph, END

from app.services.car_logic import (
    filter_by_budget,
    score_vehicle,
)


class AgentState(TypedDict):
    cars: List[Dict[str, Any]]
    budget: int
    preferences: Dict[str, Any]
    filtered: List[Dict[str, Any]]
    scored: List[Dict[str, Any]]
    result: List[Dict[str, Any]]


def filter_node(state: AgentState) -> AgentState:
    filtered = filter_by_budget(state["cars"], state["budget"])
    state["filtered"] = filtered
    return state


def score_node(state: AgentState) -> AgentState:
    scored = []

    for car in state["filtered"]:
        score = score_vehicle(car, state["preferences"])
        scored.append({**car, "score": score})

    scored = sorted(scored, key=lambda x: x["score"], reverse=True)

    state["scored"] = scored
    state["result"] = scored[:3]

    return state


def build_agent():
    graph = StateGraph(AgentState)

    graph.add_node("filter", filter_node)
    graph.add_node("score", score_node)

    graph.set_entry_point("filter")

    graph.add_edge("filter", "score")
    graph.add_edge("score", END)

    return graph.compile()


agent = build_agent()


def run_agent(cars, budget, preferences):
    initial_state: AgentState = {
        "cars": cars,
        "budget": budget,
        "preferences": preferences,
        "filtered": [],
        "scored": [],
        "result": [],
    }

    final_state = agent.invoke(initial_state)
    return final_state["result"]

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class AgentTask:
    id: str
    title: str
    status: str = "pending"


@dataclass
class TaskBoard:
    items: list[AgentTask] = field(default_factory=list)
    _seq: int = 0

    def plan(self, titles: list[str]) -> list[AgentTask]:
        self.items = []
        self._seq = 0
        for title in titles:
            text = title.strip()
            if not text:
                continue
            self._seq += 1
            self.items.append(AgentTask(id=f"T{self._seq}", title=text))
        return self.items

    def update(self, task_id: str, status: str) -> AgentTask | None:
        allowed = {"pending", "in_progress", "done", "blocked"}
        if status not in allowed:
            return None
        for item in self.items:
            if item.id == task_id:
                item.status = status
                return item
        return None

    def as_lines(self) -> list[str]:
        if not self.items:
            return ["任务板为空。请先 plan_tasks。"]
        return [f"{item.id} [{item.status}] {item.title}" for item in self.items]

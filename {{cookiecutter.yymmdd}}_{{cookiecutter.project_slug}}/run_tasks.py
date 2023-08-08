from __future__ import annotations
from dataclasses import dataclass
from functools import partial
from typing import Callable, Union

import click

from hal.cluster import blocking_cluster
from hal.config import cfg


@dataclass
class Task(object):
    name: str

    task: Callable


@dataclass
class TaskNode(object):
    name: str

    prompt: str

    children: Union[list[Task], list[TaskNode]]

    def __iter__(self):
        return self.children.__iter__()

    def __len__(self):
        return self.children.__len__()

    def __getitem__(self, item):
        return self.children.__getitem__(item)


names = cfg.clusters.keys()
tasks = [
    partial(blocking_cluster, cluster_cfg) for cluster_cfg in cfg.clusters.values()
]

cluster_node = TaskNode(
    prompt="Which cluster?",
    name="Start a cluster",
    children=[
        Task(name=name, task=partial(blocking_cluster, config))
        for name, config in cfg.clusters.items()
    ],
)


top_node = TaskNode(
    prompt="What would you like to do?",
    name="Top level",
    children=[
        Task(
            name="Run code (Not Implemented)",
            task=lambda: exec(
                'raise(NotImplementedError("Running code not implemented"))'
            ),
        ),
        cluster_node,
    ],
)


def prompt(node: TaskNode) -> None:
    while isinstance(node, TaskNode):
        s = (
            f"{node.prompt}\n"
            + "0. Exit\n"
            + "\n".join([f"{i}. {t.name}" for i, t in enumerate(node, start=1)])
            + "\n"
        )

        value = click.prompt(s, type=click.IntRange(0, len(node)), prompt_suffix="")
        if value == 0:
            return
        node = node[value - 1]

    node.task()


if __name__ == "__main__":
    prompt(top_node)

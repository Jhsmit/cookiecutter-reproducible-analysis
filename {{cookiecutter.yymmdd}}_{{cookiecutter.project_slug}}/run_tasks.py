from __future__ import annotations


import textwrap
from dataclasses import dataclass
from functools import partial
from typing import Callable, Union

import click

from hal.cluster import blocking_cluster
from hal.config import cfg
from hal.tasks import run_black, run_mypy, run_flake8, run_pylint, run_isort


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
tasks = [partial(blocking_cluster, cluster_cfg) for cluster_cfg in cfg.clusters.values()]

cluster_node = TaskNode(
    prompt="Which cluster?",
    name="Start a cluster",
    children=[Task(name=name, task=partial(blocking_cluster, config)) for name, config in cfg.clusters.items()]
)

code_quality = {
    'lack': run_black,
    'mypy': run_mypy,
    'flake8': run_flake8,
    'pylint': run_pylint,
    'isort': run_isort
}

quality_node = TaskNode(
    prompt="Which One?",
    name="Formatting/linting/type checking",
    children=[Task(name=k, task=v) for k, v in code_quality.items()]
)

top_node = TaskNode(
    prompt="What would you like to do?",
    name="Top level",
    children=[
        Task(name="Run code (Not Implemented)", task=lambda: exec('raise(NotImplementedError("Running code not implemented"))')),
        cluster_node,
        quality_node
    ]
)


def prompt(node: TaskNode) -> None:
    while isinstance(node, TaskNode):
        s = f"{node.prompt}\n" + \
            "0. Exit\n" + \
            "\n".join([f"{i}. {t.name}" for i, t in enumerate(node, start=1)]) + "\n"

        value = click.prompt(s, type=click.IntRange(0, len(node)), prompt_suffix="")
        if value == 0:
            return
        node = node[value - 1]

    node.task()


if __name__ == '__main__':
    prompt(top_node)

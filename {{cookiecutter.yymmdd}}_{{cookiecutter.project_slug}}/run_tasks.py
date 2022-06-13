import click
from hal.tasks import *
from hal.config import cfg
from hal.cluster import blocking_cluster
import textwrap

if __name__ == '__main__':

    # implement OOP; recursive until hitting some callable?
    # if only one option -> do that immediatly

    s = """
    What would you like to do?
    1. Run code
    2. Start a cluster
    3. Quality control
    """

    s = textwrap.dedent(s.lstrip("\n"))
    value = click.prompt(s, type=int)

    if value == 1:
        ...
        click.echo("Not implemented")
        # TODO
        # 1 run all (+start all clusters ? )

        # 2 per script
            # 1. data
            # 2. model
            # 3. view
                # 01 ....
    elif value == 2:
        q = "Which cluster?"
        options = list(cfg.clusters.keys())
        option_text = [f"{i}. {option}" for i, option in enumerate(options, start=1)]
        text = "\n".join([q] + option_text + [""])

        value = click.prompt(text, type=int)

        cluster_cfg = cfg.clusters[options[value - 1]]
        #todo move blocking part here
        blocking_cluster(cluster_cfg)

    elif value == 3:
        print("TODO: add isort")
        s = """
        Which function?
        1. black
        2. mypy
        3. flake8
        4. pylint
        5. isort
        """

        s = textwrap.dedent(s.lstrip("\n"))
        value = click.prompt(s, type=int)

        if value == 1:
            run_black()
        elif value == 2:
            run_mypy()
        elif value == 3:
            run_flake8()
        elif value == 4:
            run_pylint()
        elif value == 5:
            run_isort()
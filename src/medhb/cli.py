from pathlib import Path

import typer

app = typer.Typer()


@app.command()
def main():
    pass


@app.command()
def run(
    caseid: int,
    exe: bool = False,
    agent: Path = Path("codex"),
    prompt: str = (
        "MCP is everything you need."
        " You should not perform any local file reads, terminal commands, or online searches."
        " If you encounter errors with MCP, report immediately and exit."
    ),
) -> str | None:
    if '"' in prompt:
        raise ValueError("Prompt should not contain double quotes.")

    match agent.name:
        case "codex":
            prefix = [
                "exec",
                "--sandbox=workspace-write",
            ]
            postfix = []
        case "pi":
            prefix = ["-p"]
            postfix = []
        case _:
            raise NotImplementedError(f"Unsupported agent: {agent}")

    PROMPT = (
        f"Use and only use resources from MCP 'medhb' to diagnose patient with caseid {caseid}."
        f" Save your final results in case{caseid}.txt. {prompt}"
    )
    cmd = (
        [
            f"LANGFUSE_TRACING_ENVIRONMENT=medhb-{agent.name}",
            agent.expanduser().as_posix(),
        ]
        + prefix
        + [f'"{PROMPT}"']
        + postfix
    )
    if exe:
        import os

        os.system(" ".join(cmd))  # ty: ignore[deprecated]
    else:
        from rich.console import Console
        from rich.syntax import Syntax

        Console().print(Syntax(" ".join(cmd), "bash", word_wrap=True))

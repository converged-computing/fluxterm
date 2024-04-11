import os

import fluxterm.defaults as defaults
import fluxterm.utils as utils


def make_commands():
    """
    Read in commands from yaml
    """
    data = utils.read_yaml(os.path.join(defaults.assets_dir, "flux-commands.yaml"))[
        "commands"
    ]
    lines = ["# Flux Commands"]
    for command in data:
        lines.append(f"\n## {command['name']}")
        for group in command["groups"]:
            lines.append(f"\n### {group['name']}\n")
            for example in group["items"]:
                lines.append(example["title"] + "\n")
                lines.append(f"\n```bash\n{example['command']}\n````")
    markdown = "\n".join(lines)
    return markdown, data

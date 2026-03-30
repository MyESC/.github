#!/usr/bin/env python3
"""Update profile/README.md with latest project statistics.

Usage:
    python3 update_readme.py <projects_list_file> <stats_table_file> <readme_file>
"""

import re
import sys


def update_readme(projects_list_file, stats_table_file, readme_file):
    with open(projects_list_file, "r") as f:
        projects_list = f.read().strip()

    with open(stats_table_file, "r") as f:
        stats_lines = f.read().strip().split("\n")
    # stats_table.md starts with 2 header lines; keep only data rows
    stats_rows = "\n".join(stats_lines[2:]) if len(stats_lines) > 2 else ""

    with open(readme_file, "r") as f:
        content = f.read()

    # Update the "主要项目" (Main Projects) section between its heading and the next heading
    content = re.sub(
        r"### 主要项目\n\n(?:- [^\n]*\n)*\n### 项目特点",
        f"### 主要项目\n\n{projects_list}\n\n### 项目特点",
        content,
    )

    # Update the "项目统计" (Project Statistics) table:
    # matches the section heading, column header row, separator row, and any existing data rows
    content = re.sub(
        r"### 项目统计\n\n\| 项目[^\n]*\n\|[-| ]+\n(?:\|[^\n]*\n)*",
        (
            "### 项目统计\n\n"
            "| 项目 | 星标 | Forks | 主要语言 | 最后更新 |\n"
            "|------|------|-------|----------|----------|\n"
            f"{stats_rows}\n"
        ),
        content,
    )

    with open(readme_file, "w") as f:
        f.write(content)

    print("README.md updated successfully")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} <projects_list_file> <stats_table_file> <readme_file>")
        sys.exit(1)
    update_readme(sys.argv[1], sys.argv[2], sys.argv[3])

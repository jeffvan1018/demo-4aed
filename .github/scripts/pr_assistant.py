# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "google-antigravity>=0.1.20",
# ]
# ///

import asyncio
import os
import subprocess
import sys

from google.antigravity import Agent, LocalAgentConfig

async def main():
    pr_number = os.environ.get("PR_NUMBER")
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    gcp_project = os.environ.get("GCP_PROJECT_ID")
    gcp_location = os.environ.get("GCP_LOCATION", "global")
    model_name = os.environ.get("MODEL_NAME", "gemini-3.8-flash")

    if not pr_number:
        print("Missing PR_NUMBER environment variable.", file=sys.stderr)
        sys.exit(1)

    if not gcp_project:
        print("Missing GCP_PROJECT_ID environment variable.", file=sys.stderr)
        sys.exit(1)

    diff = subprocess.check_output(
        ["gh", "pr", "diff", pr_number],
        text=True
    )

    prompt = (
        f"Review this PR diff and output a brief summary, issues found, "
        f"and end with 'VERDICT: PASS' or 'VERDICT: FAIL':\n\n{diff[:8000]}"
    )

    config = LocalAgentConfig(
        vertex=True,
        project = gcp_project,
        location = gcp_location,
        model=model_name
    )

    async with Agent(config) as agent:
        response = await agent.chat(prompt)
        review_text = await response.text()

    if summary_path:
        with open(summary_path, "a", encoding="utf-8") as f:
            f.write(f"## Antigravity Review\n\n{review_text}\n")

    subprocess.run(
        ["gh", "pr", "comment", pr_number, "--body", review_text],
        check=True
    )

    if "VERDICT: FAIL" in review_text:
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    asyncio.run(main())
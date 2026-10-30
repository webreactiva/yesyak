# Plan check hooks

The plan check of `yak-pilot` (`yak-pilot/scripts/check_plan.py` in the skills folder) runs as a hook, so the agent runs it and the model cannot skip it. With `--hook` it exits 2 on a problem, writes the problems to stderr, keeps stdout empty, and exits 0 when the hook input has `stop_hook_active` (the hook already blocked once in this turn).

Write the path of the script as it is in the project: the skills folder of the project, for example `.claude/skills` or `.agents/skills`. Each example below uses `<skills>` for it.

## An agent with a stop event that can block (for example Claude Code or Codex)

The agent runs the check when a turn ends. On a problem, the turn goes on with the problems as the next prompt.

Claude Code, in `.claude/settings.json` (merge with the hooks that are there):

```json
{
  "hooks": {
    "Stop": [
      { "hooks": [ { "type": "command", "command": "python3 \"$CLAUDE_PROJECT_DIR/<skills>/yak-pilot/scripts/check_plan.py\" --hook" } ] }
    ]
  }
}
```

Codex, in `.codex/hooks.json`. Codex runs a project hook only after the user trusts it: tell the user to open `codex` in the project and approve it in `/hooks`.

```json
{
  "hooks": {
    "Stop": [
      { "hooks": [ { "type": "command", "command": "python3 \"$(git rev-parse --show-toplevel)/<skills>/yak-pilot/scripts/check_plan.py\" --hook", "timeout": 30 } ] }
    ]
  }
}
```

## An agent with a hook before a tool call (for example OpenCode)

Block a commit or a push while the check fails. OpenCode 2, in `.opencode/plugins/yesyak-plan-check.js` (OpenCode 1 used another plugin shape):

```js
import { spawnSync } from "node:child_process"
import { fileURLToPath } from "node:url"

// The project root, two folders above .opencode/plugins/.
const root = fileURLToPath(new URL("../..", import.meta.url))

export default {
  id: "yesyak-plan-check",
  async setup(ctx) {
    ctx.tool.hook("execute.before", (event) => {
      // git options can come before the subcommand, for example git -c user.name=x commit.
      if (!["shell", "bash"].includes(event.tool) || !/\bgit\b.*\b(commit|push)\b/.test(event.input?.command ?? "")) return
      const result = spawnSync("python3", ["<skills>/yak-pilot/scripts/check_plan.py"], { cwd: root, encoding: "utf8" })
      if (result.status !== 0) throw new Error(result.stderr)
    })
  },
}
```

## Check it

After you write the hook, run the script once by hand from the project root. With no plan it prints "nothing to check" and exits 0.

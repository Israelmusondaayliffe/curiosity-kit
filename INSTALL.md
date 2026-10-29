# Install and start using Curiosity Kit

Curiosity Kit gives your AI 26 methods for research, writing, decisions, software, websites, creative work and finishing projects. Start with Chief of Staff, or choose a specialist directly. You do not need to memorise the catalog.

We recommend **ChatGPT Work, Codex or Claude Code** for work that needs files, scripts and tools. The Claude app also accepts plugins; use its Cowork workspace for heavier tasks. The Kit works across models, but each task still needs an app with the right tools and permissions. Ordinary chat is not our recommended setup for the full Kit.

You can ask the AI to handle terminal commands and explain each step. You remain in charge of installation and permissions.

## Pick your app

| App | Start here |
| --- | --- |
| Claude Code | Paste the install message below |
| Codex | Paste the install message below |
| ChatGPT Work | Download the Work ZIP and use the plugin upload flow |
| Claude app / Cowork | Download the Claude ZIP and use the plugin upload flow |

## Claude Code

Open Claude Code and paste:

```text
Install Curiosity Kit from its official repository. Run:

claude plugin marketplace add Israelmusondaayliffe/curiosity-kit
claude plugin install curiosity-kit@curiosity-kit

Then run claude plugin list and confirm the installed version and enabled state. Preserve my other plugins and settings. If a command fails, explain the actual error and help me resolve it. Tell me when to open a fresh session.
```

Review any permission request before approving it. You should see `curiosity-kit@curiosity-kit` installed and enabled. Open a fresh session, select `/curiosity-kit:chief-of-staff`, then try the check below.

## Codex

Open Codex and paste:

```text
Install Curiosity Kit from its official repository. Run:

codex plugin marketplace add https://github.com/Israelmusondaayliffe/curiosity-kit
codex plugin add curiosity-kit@curiosity-kit

Then run codex plugin list and confirm the installed version and enabled state. Preserve my other plugins and settings. If a command fails, explain the actual error and help me resolve it. Tell me when to open a fresh session.
```

Review any permission request before approving it. You should see `curiosity-kit@curiosity-kit` in the installed plugin list. Open a fresh session and select Chief of Staff from the installed skill catalog.

Both CLIs also accept a local repository: clone or download this repository, then run the marketplace command with `.` as its source from the repository root. This is a fallback when the app can read a local copy but cannot add the remote marketplace.

There are 26 packaged skills. Codex may list only 21 for automatic selection: AI Film Studio, Gauntlet, Operating Graph, ProofLoop and the Matt method library require explicit selection. Review hooks separately through the host's controls. Trusting a hook permits it to run; it does not prove that it ran successfully.

## ChatGPT Work

1. [Download the Work ZIP](https://raw.githubusercontent.com/Israelmusondaayliffe/curiosity-kit/main/downloads/curiosity-kit-chatgpt.zip). Keep `curiosity-kit-chatgpt.zip` zipped.
2. Open the plugin upload flow available to your account. Eligible workspace owners and administrators can use **Admin console > select workspace > Plugins > Add > Upload plugin**. Other accounts may expose upload in Plugins.
3. Choose the ZIP, review it and install it. You should see Curiosity Kit in your installed plugins.
4. Start a fresh Work chat and select Curiosity Kit using the plugin picker or `@` mention. Try the check below.

Upload access varies by account, workspace and role. If the control is absent, ask Work to explain the supported installation route in your current app, or ask your workspace owner. Attaching the ZIP to an ordinary message alone does not establish installation. See [OpenAI's upload guidance](https://help.openai.com/en/articles/20001256-plugins-in-chatgpt).

## Claude app / Cowork

1. [Download the Claude ZIP](https://raw.githubusercontent.com/Israelmusondaayliffe/curiosity-kit/main/downloads/curiosity-kit-claude.zip). Keep `curiosity-kit-claude.zip` zipped.
2. Open **Customize > Plugins**, then the custom-plugin upload option, and choose the ZIP. Plugins require a supported paid plan.
3. Review and install it. You should see Curiosity Kit in your plugin list.
4. Start a fresh chat or Cowork task and select Chief of Staff through the skill picker, then try the check below.

If upload is unavailable, use **Plugins > Add > Add marketplace > Add from a repository** with `Israelmusondaayliffe/curiosity-kit`. Organisation policies may restrict sources. Ask the AI to guide you through the controls actually shown on your screen.

Claude chat supports skill instructions, while hooks and sub-agents require Cowork or Claude Code. Supported account-installed plugins can sync to Claude Code; check the actual Code session before relying on that. See [Anthropic's plugin guidance](https://support.claude.com/en/articles/13837440-use-plugins-in-claude).

## Ask the AI for help

If any route stalls, paste:

```text
Help me install Curiosity Kit from https://github.com/Israelmusondaayliffe/curiosity-kit in this app. Read its README and check the installation options actually available here. Do the steps you can, and guide me through any clicks I must do. Preserve my existing setup. Verify the installed plugin and loaded skills before saying it is ready. Explain any missing tool or permission in plain language.
```

## Check it, then do one useful task

First check the installed plugin list. In a fresh session, select Chief of Staff and ask:

```text
Use the installed Curiosity Kit Chief of Staff skill. Open its instructions and tell me which installed entry you loaded. Then turn these notes into three action items: choose a topic, draft a one-page outline, and review the outline on Friday. Keep the deadline exact and save a draft if this app supports files. Explain any tool limitation you encounter.
```

Check that the app actually loads the installed skill and produces the requested work. Naming skills from memory or from this README is not proof of installation. A successful small task proves that route works for that task, not that every provider or workflow is ready.

For your next task, give the desired result, source material, constraints and permission to make any necessary changes. Ask the AI to explain unfamiliar steps as it goes.

## Quick fixes

- **I cannot see the skill.** Check that the plugin is installed and enabled, then open a fresh session. Use the exact installed namespace `curiosity-kit`.
- **A command failed.** Give the AI the error and ask it to diagnose that error. Do not paste passwords or tokens.
- **A tool is missing.** Memory needs a separately installed Claude Mem engine. Browser checks need a browser. Image or video generation needs an available provider. Installation does not supply those services.
- **A hook did not run.** Check its registration, trust and execution in that host. Cloud and local behavior can differ; see the [hook limits](README.md#cloud-and-hooks).
- **I have an older manually uploaded ZIP.** Use the plugin's update/upload-new-version control when available. Replacing the repository download does not update an existing account installation.
- **Does the creator receive my work?** The Kit has no creator-operated collection endpoint. Your host, connected services and local workflow records have their own data handling. Read the [full disclosure](README.md#data-handling).

If you need help, record the app, step, exact error and what happened after the attempted fix. A fix is confirmed when it works on your own screen. Keep personal beta feedback private; publish only general fixes and quotations you have permission to share.

## What has been checked

The downloadable ZIPs contain version 0.1.1 and match the corresponding committed host packages file for file. The repository builder validates both combined packages and all standalone skill packages. CLI syntax was checked against the installed tools on October 28, 2026.

These checks do not establish a fresh native ZIP installation, skill loading or hook execution in your account. Read [READINESS.md](READINESS.md) for the earlier release's evidence and limits, and use the small task above to check your own setup.

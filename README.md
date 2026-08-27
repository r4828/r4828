# Robert Flanagan

Apple endpoint engineering. I write the extension attributes, configuration profiles, and shell that run across a managed Mac fleet, and I publish the parts other admins can use.

Most of it lands in one of three places.

**[mdm.tools](https://mdm.tools)** — Free browser-based builders for Mac admins. Generate dockutil commands, swiftDialog configs, PPPC profiles, Jamf smart groups, and firewall profiles without installing anything or signing up for anything. Also home to Field Notes, below.

**[macadmin-toolbox](https://github.com/r4828/macadmin-toolbox)** — MIT-licensed Jamf Pro and vendor-neutral MDM scripts that run on any Jamf tier with no external dependencies. Two extension attributes so far. One finds shadow AI across a fleet: desktop apps, CLI coding agents, editor and browser extensions, and MCP configuration, reported into the computer record so you can scope Smart Groups off it. The other inventories Intel-only application bundles ahead of the Rosetta 2 wind-down, and degrades to a partial-scan status rather than ever reporting a false clean zero. Both ship with an installer, a launchd collector, and tests. Pull requests are the whole point of the repo.

**[ci-workflows](https://github.com/r4828/ci-workflows)** — Reusable GitHub Actions workflows shared across my repositories: secret scanning and workflow auditing.

## Field Notes

Write-ups from [mdm.tools/blog](https://mdm.tools/blog/). Short, specific, and mostly about the gap between what the documentation says and what the fleet does.

<!-- FIELD-NOTES:START -->
- **[A Change Feed Is Not a Desired State](<https://mdm.tools/blog/change-feed-is-not-a-desired-state/>)** · 2026-08-26  
  Google Workspace, Linear, and Jamf Pro each answer 'what changed' differently, and none of them tell you what the approved configuration was supposed to be.
- **[macOS 27 App Data Protection: No Schema Key](<https://mdm.tools/blog/xprotect-app-data-protection-macos-27/>)** · 2026-08-16  
  Apple ships a file access policy through XProtect. On the macOS 27 beta, sandboxd looks for a different filename, ignores it, and runs its own built-in rules.
- **[Rosetta Deprecation Notice: Why It Rarely Fires](<https://mdm.tools/blog/rosetta-notice-is-not-an-inventory/>)** · 2026-08-12  
  The macOS 26.4 Rosetta notice sits behind a game filter, rate limits and a server-delivered policy. Apple documents that Intel plug-ins may not trigger it.
- **[Encrypted HFS+ Time Machine in macOS 28](<https://mdm.tools/blog/encrypted-hfs-time-machine-macos-28/>)** · 2026-08-10  
  Apple documents two fixes for encrypted Mac OS Extended volumes and excludes Time Machine backup disks from both. What is left is a new lineage.
- **[Age Signal Laws vs Managed Macs: AB 1043](<https://mdm.tools/blog/age-signal-laws-managed-macs/>)** · 2026-08-06  
  Texas went live in June, California follows in January, Illinois in 2028. Apple implements all five through one API, and an ADE-enrolled Mac is outside it.
<!-- FIELD-NOTES:END -->

## What I'm working on

- Declarative device management, and what macOS 27 changes about enforcing software updates
- Platform SSO, including where the passwordless story stops and the FileVault unlock constraints start
- Testing fleet scripts against clean throwaway macOS VMs instead of hoping
- Closing the distance between a script that works on my Mac and a script that works on every Mac

## Elsewhere

- [mdm.tools](https://mdm.tools) — builders and Field Notes
- [Field Notes RSS](https://mdm.tools/blog/feed.xml)
- Issues and pull requests on [macadmin-toolbox](https://github.com/r4828/macadmin-toolbox/issues) are the fastest way to reach me about a script

# HTB Academy Android Application Pentesting Path Scraper

## Mission

Extract all educational content from the HTB Academy Android Application Pentesting path (path ID 420) into structured Markdown study notes, then generate operational Claude Code skill files in `~/.claude/skills/` tuned for real Android pentest engagements.

This path contains seven modules. Module IDs are pre discovered, so skip path discovery and go directly to module extraction.

## Path Modules (pre discovered)

| # | Module ID | Title | Difficulty | Duration | Tier |
|---|-----------|-------|------------|----------|------|
| 01 | 195 | Android Fundamentals | Fundamental | 1d | Tier 0 |
| 02 | 221 | Android Application Static Analysis | Medium | 2d | Tier III |
| 03 | 249 | Android Application Dynamic Analysis | Medium | 2d | Tier III |
| 04 | 272 | Android Application Malware Analysis | Hard | 1d | Tier III |
| 05 | 281 | Android Penetration Testing Automation | Medium | 1d | Tier III |
| 06 | 288 | Android Forensics | Medium | 1d | Tier III |
| 07 | 340 | Android Attacks | Medium | 1d | Tier III |

Path URL: `https://academy.hackthebox.com/app/paths/420/path-progress`

## Output Directory Layout

```
~/dev/htb-android-pentest/
├── CLAUDE.md                    (this file)
├── 00-INDEX.md                  (progress tracker)
├── images/                      (downloaded module images, organized by module)
│   ├── 01-fundamentals/
│   ├── 02-static-analysis/
│   └── ...
├── 01-android-fundamentals.md
├── 02-static-analysis.md
├── 03-dynamic-analysis.md
├── 04-malware-analysis.md
├── 05-pentest-automation.md
├── 06-forensics.md
└── 07-android-attacks.md
```

## Step 1: Cookie Setup

Ask the user once for HTB session cookies:

```
I need your HTB Academy session cookies to access content. Open academy.hackthebox.com in Chrome, press F12, go to Console, and run:
document.cookie
Paste the entire output.
```

Store as environment variable for the session:

```bash
export HTB_COOKIE="<pasted full cookie string>"
```

Install dependencies once:

```bash
pip install beautifulsoup4 html2text requests --break-system-packages 2>/dev/null
```

## Step 2: Per Module Extraction

Process modules sequentially in order 01 through 07. Do not parallelize (cookie sessions can race).

### 2a. Discover sections for the module

```bash
curl -s -b "$HTB_COOKIE" "https://academy.hackthebox.com/module/details/<MODULE_ID>" > /tmp/htb_module.html

python3 << 'PYEOF'
from bs4 import BeautifulSoup
import re, json

with open('/tmp/htb_module.html') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

sections = []
for link in soup.find_all('a', href=re.compile(r'/section/\d+')):
    sid = re.search(r'/section/(\d+)', link['href'])
    if sid:
        title = link.get_text(strip=True) or 'Untitled'
        sections.append({'id': sid.group(1), 'title': title})

seen = set()
unique = []
for s in sections:
    if s['id'] not in seen:
        seen.add(s['id'])
        unique.append(s)

print(json.dumps(unique, indent=2))
PYEOF
```

If the selector fails (HTB markup changes occasionally), inspect `/tmp/htb_module.html` and adapt. Common patterns: section IDs in `<a>` href, in `data-id` attributes, or in inline JSON within `<script>` tags.

### 2b. Extract each section content

```bash
curl -s -b "$HTB_COOKIE" "https://academy.hackthebox.com/module/<MODULE_ID>/section/<SECTION_ID>" > /tmp/htb_section.html

python3 << 'PYEOF'
import html2text
from bs4 import BeautifulSoup

with open('/tmp/htb_section.html') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

content = (soup.find('div', class_='training-module')
           or soup.find('main')
           or soup.find('article'))

if content:
    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = False
    h.body_width = 0
    print(h.handle(str(content)))
PYEOF
```

### 2c. Extract relevant images

Download diagrams, architecture images, attack flow visualizations. Skip logos, decorative banners, and stock photos.

```bash
mkdir -p ~/dev/htb-android-pentest/images/<NN>-<slug>/
curl -s -b "$HTB_COOKIE" "<IMAGE_URL>" -o ~/dev/htb-android-pentest/images/<NN>-<slug>/<image_name>
```

Reference images in the MD using relative paths: `![Description](images/02-static-analysis/manifest-flow.png)`

### 2d. Extract lab solutions

Filip has Gold Annual subscription, so lab walkthroughs are unlocked. Find the solution endpoint in the section HTML and fetch it. Include full solution commands, expected outputs, and flag values in the MD file.

## Step 3: Module Markdown Template

Mobile content has different artifacts than web content. Use this template tuned for Android, not the generic web template:

```markdown
# <NN>. <Module Title>

> **Difficulty:** <value> | **Duration:** <value> | **Tier:** <value>  
> **Module ID:** <id>

## What This Covers

Full module description. Do not summarize. Preserve all explanatory text from the source.

## Real World Relevance

Concrete scenarios where these techniques apply. Reference real CVEs (Strandhogg, Janus, Cloak and Dagger, Pegasus delivery vectors, banking trojans like Anatsa or BRATA) when the module touches related techniques.

## Core Concepts

### <Concept Name>

**Definition:** ...

**Internals:** How this works at the Android framework level (binder IPC, zygote, ART runtime, SELinux contexts, AID model, app sandbox boundaries, etc.).

**Why it matters offensively:** What an attacker gains by understanding this.

Include all code snippets, AndroidManifest.xml fragments, smali patterns, Java/Kotlin source, Frida hook examples, native library disassembly, and protocol details verbatim from the source.

## Setup and Tooling

### Required tools per section

List tools used in this module: apktool, jadx, MobSF, Frida, Objection, ADB, Burp Suite Pro, drozer, mitmproxy, Genymotion, magisk modules, etc.

### Environment

Genymotion vs physical device guidance, Android version requirements, root status, Frida server setup, certificate installation procedure (network_security_config.xml, magisk MoveCertificates module, etc.).

## Attack Techniques

### <Technique Name>

**Goal:** What the attacker achieves.

**Prerequisites:** App with attribute X enabled (exported activity, debuggable flag, etc.), device with API level Y, root status, custom app installed, etc.

**Steps:**
1. Static recon (apktool d, jadx, MobSF scan)
2. Locate target (smali class, content provider URI, exported activity, deep link host, intent filter)
3. Craft payload (intent extras, adb am start command, custom calling app, malicious deep link URL, etc.)
4. Execute and verify

**Detection in code:**

```smali
<smali pattern that indicates this vulnerability>
```

```java
<Java/Kotlin source pattern>
```

```xml
<AndroidManifest fragment>
```

**Frida hook example:**

```javascript
Java.perform(function() {
  var Target = Java.use("com.example.TargetClass");
  Target.method.implementation = function() {
    console.log("[+] Hooked method called");
    return this.method.apply(this, arguments);
  };
});
```

**Objection commands:**

```
android hooking list classes
android hooking watch class_method com.example.Class.method
android sslpinning disable
android root disable
android intent launch_activity com.example.target.SecretActivity
```

**ADB commands:**

```bash
adb shell am start -n com.example/.SecretActivity
adb shell content query --uri content://com.example.provider/users
```

**Pitfalls:** Common reasons this fails (anti debugging via ptrace, root detection via su binary check, certificate pinning via TrustManager, native code obfuscation, RASP solutions like Promon Shield) and bypass approach.

## MASVS and MASTG Mapping

Map every covered technique to MASVS controls and MASTG test cases. This makes the content immediately reusable in client reports for Filip's mobile pentest engagements.

| Technique | MASVS Control | MASTG Test |
|---|---|---|
| Hardcoded API key | MSTG-STORAGE-1 | MASTG-TEST-0001 |
| Disabled SSL pinning | MSTG-NETWORK-4 | MASTG-TEST-0021 |
| ... | ... | ... |

## Lab Walkthroughs

Each lab from the module with full solution.

### Lab: <name>

**Question:** ...

**Approach:** ...

**Commands:**

```bash
<full commands verbatim>
```

**Expected output:**

```
<full output>
```

**Flag:** ...

## References

External links, Android docs, OWASP MASTG sections, blog posts, CVE references referenced in the module.
```

## Step 4: Skill Generation

After all seven module MDs are written, generate skill directories in `~/.claude/skills/`. Skills are operational, not educational. Decision trees, not textbooks. Reusable in real client engagements.

### Suggested skill set

Read all module content first, then cluster by offensive capability (not by module). One skill per coherent capability. Refine based on actual content discovered.

| Skill name | Source modules | Purpose |
|---|---|---|
| `android-environment-setup` | 195 | Genymotion setup, ADB workflow, Frida server install, Burp CA install via magisk, common emulator quirks |
| `android-static-analysis` | 221 | apktool/jadx workflow, AndroidManifest review, smali reading patterns, hardcoded secrets hunting, MobSF static scan |
| `android-dynamic-analysis` | 249 | Frida hooks, Objection runtime instrumentation, traffic interception, SSL pinning bypass, root detection bypass |
| `android-deep-links` | 340 | Intent scheme analysis, exported activity abuse, deep link hijacking, App Links verification |
| `android-content-providers` | 340 | Content provider enumeration, SQL injection via provider, path traversal, permission bypass |
| `android-webview-attacks` | 340 | JavaScript bridge abuse, file:// access, addJavascriptInterface RCE, mixed content, custom URL scheme handling |
| `android-storage-attacks` | 221, 249 | World readable files, shared preferences inspection, external storage misuse, keystore inspection |
| `android-malware-analysis` | 272 | Triage workflow, IOC extraction, family identification, packer detection, dropper analysis |
| `android-pentest-automation` | 281 | MobSF API automation, frida trace patterns, Drozer modules, batch APK analysis |
| `android-forensics` | 288 | ADB backup analysis, memory acquisition, app data extraction, timeline reconstruction |

### SKILL.md format

Every skill follows agent skills open standard. Keep SKILL.md under 500 lines. Move payload libraries, extended technique catalogs, and tool deep dives to `references/`. Put reusable scripts in `scripts/`.

```yaml
---
name: <skill-name>
description: "<What it does. When Claude should use it. Max 1024 chars.>"
---
```

Body structure:

```markdown
# <Skill Title>

## When to Use

One or two sentences describing the trigger condition.

## Decision Tree

If condition A, do X.  
If condition B, try Y first, then Z.  
If anti tampering or RASP detected, escalate to references/bypass.md.

## Quick Commands

Top five to ten commands the user runs in 90 percent of engagements.

## Detection Patterns

Code patterns (smali, Java, manifest XML) that indicate the vulnerability.

## Exploitation Steps

Numbered steps with copy ready commands.

## Common Pitfalls

What goes wrong and how to recover.

## References

Pointers to references/ and scripts/ within this skill directory.
```

### Critical rule: never overwrite

If a skill directory already exists in `~/.claude/skills/`, read the existing SKILL.md first and merge new content. Add a section if the topic is not covered. Do not delete existing content. Bump frontmatter description if scope expanded.

## Step 5: 00-INDEX.md Tracker

Maintain `~/dev/htb-android-pentest/00-INDEX.md` throughout the run:

```markdown
# Android Application Pentesting Path Progress

## Modules

- [ ] 01. Android Fundamentals (195)
- [ ] 02. Android Application Static Analysis (221)
- [ ] 03. Android Application Dynamic Analysis (249)
- [ ] 04. Android Application Malware Analysis (272)
- [ ] 05. Android Penetration Testing Automation (281)
- [ ] 06. Android Forensics (288)
- [ ] 07. Android Attacks (340)

## Skills Generated

(populated as skills are written)

## Notes

(extraction issues, missing labs, sections that need manual review)
```

Mark a module complete only after the MD file is written and contains all sections including labs. Update this file after each module.

## Execution Rules

1. Process modules in order, 01 through 07. Sequential only. Cookie sessions can race under parallel curl.
2. Save raw HTML to `/tmp/` for every section before parsing. This lets you re parse if extraction logic needs tuning later.
3. If a section returns 401 or 403, the cookie expired. Stop and ask the user for a fresh cookie.
4. Never summarize content. Extract everything. Filip will use these for CPTS adjacent prep, eMAPT refresh, and engagement reference.
5. If a lab solution is locked or fails to extract, note it in 00-INDEX.md and proceed.
6. After each module completes, update 00-INDEX.md before starting the next.
7. Skill generation runs after all seven modules are extracted. Read everything first, design the skill set, then write.
8. Resume rules: on context reset, read 00-INDEX.md, find the first incomplete module, continue from there. Re read existing skills before extending them.
9. Image filtering: download diagrams, architecture, attack flows. Skip logos, decorative banners, stock photos, and stock illustrations.
10. Never invent content. If a section is empty or behind a paywall, mark it explicitly and move on.
11. Filip's writing style: avoid em dashes, en dashes, and inline hyphens. Use commas, semicolons, periods.
12. Do not use these words anywhere in extracted notes or skill files: delve, tapestry, vibrant, landscape, realm, embark, excels, vital, comprehensive, intricate, pivotal, moreover, arguably, notably, robust, seamless, cutting edge, state of the art, unparalleled, game changing, revolutionary, synergy, empower, unleash. Rewrite if the source uses them.

## Start

Once `HTB_COOKIE` is set, begin with module 195 immediately. Proceed without further prompting.

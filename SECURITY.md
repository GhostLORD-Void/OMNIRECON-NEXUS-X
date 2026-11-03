# Security Policy

## Supported use
OMNIRECON NEXUS X is a development foundation. Use security-related capabilities only on systems you own or have explicit written permission to assess.

## Current boundaries
- The task planner produces plans; it does not launch scans or run commands.
- No arbitrary shell or generated-code execution is provided.
- The model adapter returns text only and does not grant the model tool access.
- Tool policies default to disabled and require explicit authorization checks.
- Do not expose the API or dashboard publicly without authentication, TLS, rate limiting, and deployment review.

## Reporting
Do not publish secrets, tokens, personal data, or exploitable details in public issues. Contact the repository maintainer privately with a concise reproduction and impact description.

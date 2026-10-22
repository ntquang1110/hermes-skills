# Multi-Agent Patent Cross-Validation Protocol

Used 24/09/2026 for guava leaf tanin powder patent analysis. Confirmed effective: 2 parallel agents caught issues neither alone would have.

## When to use

User asks "can I patent this combination/process/product?" — the deliverable is a patentability opinion, not a deep-dive reproduction of an existing patent.

## Agent roles

### Agent 1 — Patent Examiner / IP Specialist
- Reads actual claims from Google Patents (curl HTML, extract claims section)
- Applies problem-and-solution framework: closest prior art → differences → objective technical problem
- Builds novelty matrix (element × document)
- Assesses inventive step under local law (Điều 61-62 Luật SHTT VN or equivalent EPC 54/56)
- Drafts sample independent + dependent claims
- Flags infringement risk against active patents

### Agent 2 — Domain Technical Expert
- Evaluates chemical/process feasibility of transferring known steps to the new context
- Identifies hidden critical parameters (pH, ionic strength, temperature, solvent composition)
- Checks for synergistic effects vs mere aggregation
- Validates whether claimed product specs are achievable given mass balance constraints
- Flags safety/regulatory issues (residual solvents, heavy metals, halal, fire/explosion)

## Workflow

1. **Dispatch parallel** — both agents get the same proposed invention description + full prior art list. Each reads actual patent claims independently. Do NOT share context between them (they must not influence each other).

2. **Wait for both to complete** — each writes its own report file. Do not synthesize until both are back.

3. **Synthesize** — identify:
   - **Convergent findings**: both agree → high confidence, use as primary conclusions
   - **Divergent findings**: one says novel, other says not → investigate the gap
   - **Unique findings per agent**: these are the most valuable — each agent's specialist angle

4. **Correction table** — compare the user's own description of each prior art patent against the actual claims. Document every discrepancy. This is critical: this session found 4/4 descriptions were wrong.

5. **Build deliverable** — HTML with:
   - Executive verdict (scored: novelty, inventive step, industrial applicability, infringement risk)
   - Correction table (what the user thought vs what claims actually say)
   - Novelty matrix
   - Problem-and-solution inventive step analysis
   - Draft claims (independent process + independent product)
   - Risk assessment with mitigation
   - Why it can be protected (3-4 concrete arguments)

## Pitfalls

- **Secondary descriptions are unreliable.** Always read actual claims. This session found 4 critical errors in the user's own R&D document. The worst: EP2022343B1 was described as "maltodextrin + spray drying" — actual claim is freeze drying. This single error would have invalidated the entire analysis.
- **Technology transfer is not obvious.** A step that works in one context (e.g., IPA phase separation for tanning waste with high ionic strength) may fail in another (guava leaf extract with low ionic strength). The chemist agent must evaluate this.
- **Claim scope creep.** Don't let the user claim more than the data supports. If the product spec (40-55% tannin) may not be achievable, flag it as a risk, don't write it into the claim.
- **Infringement risk is separate from patentability.** A process can be novel AND infringe an existing patent. Always check both.

## Output structure (HTML)

- Masthead: edition metadata, title
- Executive verdict: 4 scored boxes (Novelty, Inventive Step, Applicability, Infringement Risk)
- Section 1: Correction table (user's description vs actual claims)
- Section 2: Prior art list (6+ documents with status)
- Section 3: Novelty matrix (steps × documents)
- Section 4: Corrected process flow with critical parameters
- Section 5: Problem-and-solution inventive step analysis
- Section 6: Draft claims (independent + dependent)
- Section 7: Why patentable (3-4 arguments with legal basis)
- Section 8: Risk assessment + mitigation

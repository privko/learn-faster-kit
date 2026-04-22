---
description: Initialize or continue learning a programming topic using project-based approach
---

## Context

- Topic to learn: $ARGUMENTS
- Current topic: !`ls .learning/ 2>/dev/null | grep -v scripts`

**Note:** The `.learning/` directory is already initialized. Check the topic folder name (ignore `scripts/`).

## Your Task

Initialize learning for the topic "$ARGUMENTS" using the FASTER framework with project-based approach.

**If a topic already exists:**

- Inform: "This project is already learning [topic name]"
- Check for due reviews first (conduct before new learning if any)
- Continue with current topic (1 project = 1 learning goal)

**If no topic exists yet:**

1. **Gather learning preferences** by asking the user directly:

Ask: "What level do you want to achieve with [topic]? Reply with:
- **Beginner** - Fundamentals and basic syntax
- **Intermediate** - Common patterns and projects
- **Advanced** - Architecture and optimization
- **Expert** - Deep internals and best practices"

Ask: "What's your learning goal? (select all that apply) Reply with:
- **Build projects** - Learn by building real applications
- **Understand deeply** - How things work under the hood
- **Best practices** - Production-ready code patterns
- **Interview prep** - Problem-solving and algorithms"

2. Run: `python3 .learning/scripts/init_learning.py "[topic name]" .learning`
3. Parse JSON output and follow `llm_directive`
4. **READ** `.learning/<topic-slug>/syllabus.md` to see the template structure
5. Generate comprehensive syllabus **focused on project-based learning**
6. **Replace** the template placeholders with actual content
7. Update metadata: `"syllabus_generated": true` in `.learning/<topic-slug>/metadata.json`

**Programming Mode Syllabus Guidelines:**

- Structure around building progressively complex projects
- Each phase should include 2-3 concepts + 1-2 🔨 hands-on projects
- Projects should build on previous concepts
- Include testing and debugging at each phase
- Focus on understanding "how it works" not just "how to use it"
- Use checkboxes `- [ ]` for tracking progress

**Important:**

- Generate comprehensive, project-focused syllabi
- Every concept should lead to building something
- Include code quality and best practices throughout

---
description: Initialize a new learning topic or continue learning an existing one using the FASTER framework
---

## Context

- Topic to learn: $ARGUMENTS
- Current topic: !`ls .learning/ 2>/dev/null | grep -v scripts`

**Note:** The `.learning/` directory is already initialized. Check the topic folder name (ignore `scripts/`).

## Your Task

Initialize learning for the topic "$ARGUMENTS" using the FASTER framework.

**If a topic already exists:**

- Inform: "This project is already learning [topic name]"
- Check for due reviews first (conduct before new learning if any)
- Continue with current topic (1 project = 1 learning goal)

**If no topic exists yet:**

1. **Gather learning preferences** by asking the user directly:

Ask: "What level do you want to achieve with [topic]? Reply with:
- **Beginner** - Fundamentals and basic concepts
- **Intermediate** - Practical skills and common patterns
- **Advanced** - Deep expertise and edge cases
- **Expert** - Mastery level, architecture, optimization"

Ask: "What do you want to focus on? (select all that apply) Reply with:
- **Theory** - Concepts, principles, how things work
- **Practice** - Hands-on coding and building projects
- **Real-world** - Production patterns and best practices
- **Interview prep** - Common questions and problem-solving"

2. Run: `python3 .learning/scripts/init_learning.py "[topic name]" .learning`
3. Parse JSON output and follow `llm_directive`
4. **READ** `.learning/<topic-slug>/syllabus.md` to see the template structure
5. Generate comprehensive syllabus content **tailored to user's level and focus areas**
6. **Replace** the template placeholders with actual content
7. Update metadata: `"syllabus_generated": true` in `.learning/<topic-slug>/metadata.json`

**Follow the template structure:**

- All sections from the template file (Overview, Prerequisites, Learning Objectives, etc.)
- 3-4 Phases with specific concepts + 🔨 hands-on projects
- Checkboxes `- [ ]` for tracking progress

**Important:**

- Generate comprehensive syllabi (not minimal)
- Include hands-on practice in every phase

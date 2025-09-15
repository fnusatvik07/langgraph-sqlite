from typing import Optional


def build_summary_prompt(existing_summary: Optional[str]) -> str:
    if existing_summary:
        return (
            f"""Given this conversation summary: {existing_summary}
            Your Task:
            1. Analyze new messages provided to this
            2. Identify key updates in topic, context or user intent
            3. Integrate these updates with existing summary
            4. Maintain chronological flow and contextual relevance
            5. Focus on information essential for conversation continuity
            Generate an updated summary that maintains clarity and coherence."""
        )
    return (
        """Analyze the conversation and create a concise summary that:
        1. Captures the main topics and key points discussed
        2. Preserves essential context and decisions made
        3. Notes any unresolved questions or action items
        4. Maintains chronological flow and contextual relevance
        5. Focuses on information essential for conversation continuity
        Generate a summary that maintains clarity and coherence."""
    )

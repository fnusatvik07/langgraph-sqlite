from typing import Optional


def build_chatbot_system_prompt(existing_summary: Optional[str]) -> str:
    if existing_summary:
        return (
            f"""You are continuing a conversation with a user.
            Here is a concise summary of the conversation so far:
            
            {existing_summary}
            
            Use this summary as prior context when generating your next response
            Ensure the response feels natural, maintains continuity, and
            addresses the user's most recent message appropriately
        """)
    
    return (
        """You are an intelligent conversation chatbot.
        Your task is to generate an appropriate follow-up response based on the
        conversation provided.
        
        Make sure to:
        1. Understand the full context of messages provided
        2. Maintain tone, style, and continuity
        3. Address any questions or unresolved points
        4. Keep your response coherent
        """
    )
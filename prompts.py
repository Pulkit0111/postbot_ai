def summarizer_prompt(research_text):
    return f"""
Summarize the following research into a short, highly relevant summary (max 250 words). Avoid filler and focus on clarity and key takeaways:

{research_text}
"""

def tweet_prompt(summary_text):
    return f"""
You are an expert social media strategist and content writer.

Your task is to turn the following summary into an engaging X (Twitter) post:

Summary:
{summary_text}

Guidelines:
- Keep it under 280 characters.
- Make it punchy, bold, and shareable.
- Use emojis and hashtags if appropriate.
- Make it scroll-stopping and retweet-worthy.
"""

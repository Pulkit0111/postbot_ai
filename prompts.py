def summarizer_prompt(research_text):
    return f"""
You are an expert content analyst and strategist.

Your task is to deeply analyze and summarize the following research content into a compact yet comprehensive summary, no longer than 250 words.

Requirements:
- Capture the **essence of every important point** or argument across the full research.
- The summary must be **self-sufficient**: it should convey all the insight required to generate a high-quality, viral social media post **without needing the original content again**.
- It should be **structured clearly** and include **key trends, numbers, or facts** if present.
- Avoid unnecessary filler or generic commentary.

Here is the research content:
{research_text}
"""

def tweet_prompt(summary_text):
    return f"""
You are an elite-level social media strategist with deep knowledge of viral content formats, trends, and hooks.

Your task is to transform the following summary into a **world-class X (Twitter) post** designed to **go viral**.

Requirements:
- Keep it **under 280 characters**.
- Use a **scroll-stopping hook** or insight up front.
- Include **trendy, relevant hashtags** and **emojis** where they amplify the message.
- Write in a **bold, punchy, conversational tone**.
- Use **current internet trends or terminology** if applicable (e.g. “insane stat,” “you won’t believe,” “here’s why”).
- Avoid generic phrasing. Make it feel **crafted for high engagement**.

Here is the summary to base the post on:
{summary_text}
"""

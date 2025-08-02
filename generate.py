from search import search_topic
from ai import get_response
from prompts import summarizer_prompt, tweet_prompt

def generate_tweet_from_topic(topic):
    research_text = search_topic(topic)
    if not research_text:
        return "❌ Could not gather research. Please try another topic."

    summary = get_response(summarizer_prompt(research_text))
    if "⚠️" in summary:
        return summary

    draft = get_response(tweet_prompt(summary))

    # Feedback loop
    while True:
        print("\n💬 Draft Tweet:\n")
        print(draft)
        feedback = input("\n📝 Feedback (or type 'done' to accept):\n")
        if feedback.lower() == "done":
            return draft
        else:
            revision_prompt = f"Rewrite the following tweet based on this feedback:\n\nTweet:\n{draft}\n\nFeedback:\n{feedback}, go theough summary again and make sure it is relevant to the topic, here is the summary: {summary}"
            draft = get_response(revision_prompt)

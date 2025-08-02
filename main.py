from generate import generate_tweet_from_topic

def main():
    print("Welcome to the Twitter Post Generator!")
    print("Enter a topic to generate a Twitter post (or type 'exit' to quit):")
    while True:
        topic = input("Topic: ")
        if topic.lower() == "exit":
            print("Exiting... Goodbye!")
            break
        else:
            final = generate_tweet_from_topic(topic)
            print(f"\n✅ Final Tweet Ready to Post:\n{final}\n")

if __name__ == "__main__":
    main()

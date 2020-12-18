import openai


def query_most_likely(query, allowed_set, print_probs=False):
    response = openai.Completion.create(engine="davinci", prompt=query, max_tokens=1, logprobs=100, n=1)
    logprobs = response['choices'][0]['logprobs']['top_logprobs'][0]
    found_actions = []
    for item in allowed_set:
        k = " " + item.lower()
        if k not in logprobs:
            continue
        # print(f"{k}: {logprobs[k]}")
        found_actions.append((logprobs[k], item))
    if print_probs:
        print(sorted(found_actions, reverse=True))
    return sorted(found_actions)[-1][1]
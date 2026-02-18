def keyword_segmentation(user_query, marketing_keywords_dictionary):
    """Return all segmentations of user_query using marketing keywords.

    Uses DFS + memoization. Returns a list of strings with words separated by spaces.
    """
    word_set = set(marketing_keywords_dictionary)
    memo = {}

    def dfs(start):
        if start in memo:
            return memo[start]
        if start == len(user_query):
            return [""]

        sentences = []
        for end in range(start + 1, len(user_query) + 1):
            word = user_query[start:end]
            if word in word_set:
                for sub in dfs(end):
                    if sub:
                        sentences.append(word + " " + sub)
                    else:
                        sentences.append(word)
        memo[start] = sentences
        return sentences

    return dfs(0)


if __name__ == "__main__":
    # Demo
    query = "applebananaapple"
    dict_words = ["apple", "banana"]
    print(keyword_segmentation(query, dict_words))

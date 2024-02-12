import os
import random
import re
import sys
import math

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    probabilities = {}

    random_choice = (1-damping_factor) * 1/len(corpus)

    if len(corpus[page]) > 0:
        for current_page in corpus:
            if current_page != page:
                probabilities[current_page] = random_choice + damping_factor * 1/len(corpus[page])
            else:
                probabilities[current_page] = random_choice
    else:
        for current_page in corpus:
            probabilities[current_page] = random_choice

    return probabilities

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    pageRank = corpus.copy()
    for page in pageRank:
        pageRank[page] = 0

    actual_page = None
    chosen_sample = None
    pages = list(pageRank.keys())

    for _ in range(n):
        if actual_page:
            prob_dict = transition_model(corpus, actual_page, damping_factor)
            weights = list(prob_dict.items())

            chosen_sample = random.choices(pages, weights, k=1)[0]

            actual_page = chosen_sample
        else:
            chosen_sample = random.choice(pages)

        pageRank[chosen_sample] += 1/n

    return pageRank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    n = len(corpus)

    pageRank = corpus.copy()
    for page in pageRank:
        pageRank[page] = 1/n

    actual_page = None
    chosen_sample = None
    pages = list(pageRank.keys())


    active = True
    while active:
        
        oldProbabilities = pageRank.copy()
        
        for page in pages:

            temp_sum = 0

            for i in pages:
                if i in corpus[page]:
                    temp_sum += damping_factor * oldProbabilities[i]/len(corpus[i])

                if len(corpus[i]) == 0:
                    temp_sum += damping_factor * oldProbabilities[i]/n
            
            temp_sum += (1-damping_factor)/n

            pageRank[page] = temp_sum

        active = False
        for page in pages:
            dif = abs(pageRank[page] - oldProbabilities[page])

            if dif > 0.001:
                active = True

    return pageRank

if __name__ == "__main__":
    main()

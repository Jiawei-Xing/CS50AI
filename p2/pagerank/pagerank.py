import os
import random
import re
import sys

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
    # randomly choose from all
    prob = {}
    for each in corpus:
        prob[each] = (1 - damping_factor) / len(corpus)
        if corpus[each] == set():
            for every in corpus:
                corpus[each].add(every)

    # choose linked pages
    for each in corpus[page]:
        prob[each] += damping_factor / len(corpus[page])

    return prob


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    sample = {}
    for each in corpus:
        sample[each] = 0

    # the first sample
    page = random.choice(list(corpus.keys()))
    sample[page] += 1 / n

    # sampling
    for i in range(n-1):
        transition = transition_model(corpus, page, damping_factor)
        page = random.choices(list(transition.keys()), list(transition.values()))[0]
        sample[page] += 1 / n

    return(sample)


def change(old, new, value = 0.001):
    """
    Return boolean values indicating whether no PageRank value changes by more than 0.001.
    """
    for i in range(len(old)):
        if abs(list(old.values())[i] - list(new.values())[i]) > value:
            return False
    return True


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # init pagerank
    pr = {}
    for each in corpus:
        pr[each] = 1 / len(corpus)
        if corpus[each] == set():
            for every in corpus:
                corpus[each].add(every)

    # iteration
    while True:
        new = {}
        for each in corpus:
            new[each] = (1 - damping_factor) / len(corpus)
            for every in corpus:
                if each in corpus[every]:
                    new[each] += damping_factor * pr[every] / len(corpus[every])

        if change(pr, new):
            return new
        else:
            pr = new.copy()


if __name__ == "__main__":
    main()

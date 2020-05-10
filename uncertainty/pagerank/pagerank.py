import os
import random
import re
import sys
import copy

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
    # Initialize dictionary of probability distributions with probability of 0
    probDist = {}
    for corpPage in corpus:
        probDist[corpPage] = 0

    # If given page has no outgoing links
    if len(corpus[page]) == 0:
        # There is an equal probability of landing on any page
        prob = round(1 / len(corpus), 3)
        for corpPage in corpus: probDist[corpPage] = prob
    else:
        probOfLandingOnOutgoingPage = round(damping_factor / len(corpus[page]), 3)
        for outgoingPage in corpus[page]:
            probDist[outgoingPage] += probOfLandingOnOutgoingPage

        probOfLandingOnAnyPage = round((1 - damping_factor) / len(corpus), 3)
        for corpPage in corpus:
            probDist[corpPage] += probOfLandingOnAnyPage

    return probDist

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    timesLandedOnPage = {}
    for page in corpus:
        timesLandedOnPage[page] = 0
    # Randomly pick one page from the corpus and increment the times we've seen it
    currPage = random.choice(list(corpus))
    timesLandedOnPage[currPage] += 1
    # Initialize sample count
    count = 0
    while True:
        # Only count as many samples as n
        if count == n:
            break
        # Get the transition model for the current page
        probDistForCurrPage = transition_model(corpus, currPage, damping_factor)
        # Get possible pages based on the transition model
        pages = list(probDistForCurrPage.keys())
        # Get the probabilities of landing on each of those pages from the current page based on transition model
        pageWeights = list(probDistForCurrPage.values())
        # Randomly choose next page based on transition model and increment the times we've seen this page
        currPage = (random.choices(pages, weights=pageWeights))[0]
        timesLandedOnPage[currPage] += 1
        # Increment sample count
        count += 1
    pageRanks = {}
    for page in timesLandedOnPage:
        pageRanks[page] = round(timesLandedOnPage[page] / n, 4)
    return pageRanks

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Initialize page ranks as equal
    pageRanks = {}
    initialPageRank = 1 / len(corpus)
    for page in corpus:
        pageRanks[page] = initialPageRank
    # Initialze empty dictionary upon which to iterate page rank values for each page
    iteratedPageRanks = {}
    while True:
        # We will update the page rank of every page
        for page in corpus:
            # Add the first term in the equation based on randomly landing on a page from the corpus
            iteratedPageRanks[page] = (1 - damping_factor) / len(corpus)
            # Determine second term in equation which is a sum (hence the for loop)
            for corpPage in corpus:
                # If a page in the corpus has an outgoing link to the page we're currently determining the 
                # iterated page rank of, then we consider it
                if page in corpus[corpPage]:
                    iteratedPageRanks[page] += (damping_factor * pageRanks[corpPage]) / len(corpus[corpPage])
                # If a page in the corpus has no outgoing links, then we interpet it as having one link for every 
                # page in the corpus (including itself)
                elif len(corpus[corpPage]) == 0:
                    iteratedPageRanks[page] += (damping_factor * pageRanks[corpPage]) / len(corpus)
                # Else check the next page
                else:
                    continue
        # If all the iterated page ranks changed by less than 0.001, then we are done
        if all((iteratedPageRanks[page] - pageRanks[page]) < 0.001 for page in corpus):
            break
        else:
            # Continue iteration 
            pageRanks = copy.deepcopy(iteratedPageRanks)
    return iteratedPageRanks
                    
if __name__ == "__main__":
    main()

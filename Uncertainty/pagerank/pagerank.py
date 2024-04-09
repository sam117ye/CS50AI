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

    # transition model
    transition = {}

    # number of links on the current page corpus{page[links]}
    links = len(corpus[page])

    for page in corpus:
        if page not in transition:
            transition[page] = (1 - damping_factor) / len(corpus)

    
    for links in corpus[page]:
        transition[page] += damping_factor / links
 
    # if a page has no links, we can pretend it has links to all pages in the corpus, including itself.
    if links == 0:
        for page in corpus:
            transition[page] += 1 / len(corpus)

    return transition
        
def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    # Keep track of how many times each page has been visited
    # Initialize all pages to 0
    visited = {}
    for webpage in corpus:
        visited[webpage] = 0

    # First choose at random from all pages
    probabilities = [1/len(corpus)] * len(corpus)
    first_choice = random.choices(population=list(corpus.keys()), weights=probabilities, k=1)[0]

    # Repeat the process for SAMPLES times, similar to the Markov chain
    choice = first_choice
    sample = 0
    while sample <= n:
        prob = transition_model(corpus, choice, damping_factor)
        choice = random.choices(population=list(prob.keys()), weights=list(prob.values()), k=1)[0]
        visited[choice] += 1
        sample += 1

    page_rank = {}
    for webpage, visited_times in visited.items():
        page_rank[webpage] = visited_times / n

    return page_rank

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    

    page_rank = {}

    # Initialize each page's page rank to the random selection probability
    for webpage in corpus:
        page_rank[webpage] = 1 / len(corpus)

    # Iterate until PageRank converges (no PR value change by more than 0.001)
    iterating = True
    while iterating:
        iterating = False
        for cur_webpage in corpus:
            old_pr = page_rank[cur_webpage]
            sum_of_link = 0

            # Sum up the link probabilities from other page to cur page
            for other_webpage in corpus:
                # If not the same page and other page link to cur page
                if cur_webpage != other_webpage and cur_webpage in corpus[other_webpage]:
                    sum_of_link += page_rank[other_webpage] / len(corpus[other_webpage])

            # Update new PR value
            new_pr = (1 - damping_factor) / len(corpus) + damping_factor * sum_of_link
            page_rank[cur_webpage] = new_pr

            # Check if still need iterating
            if abs(new_pr - old_pr) > 0.001:
                iterating = True

    return page_rank


if __name__ == "__main__":
    main()

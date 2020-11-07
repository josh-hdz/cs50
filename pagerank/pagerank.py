import os
import random
import re
import sys
import copy
import numpy as np

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
    distribution = dict()

    # Iterates through corpus to add probability(1 - alpha) equaly to all pages in corpus.
    for key in corpus:
        distribution[key] = (1 - damping_factor) / len(corpus)


    # Iterates through corpus to find the desired page(key) and adds probability(alpha) equaly to each link found in page(key).
    for key, link_list in corpus.items():
        if len(link_list) != 0:
            if key == page:
                for link in link_list:
                    distribution[link] += damping_factor / len(link_list)

                return distribution
        else: # when link_list is empty.
            for key in corpus:
                distribution[key] += damping_factor / len(corpus)

            return distribution

    
            
    raise NotImplementedError


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    sample_list = []
    distribution = {}
    
    # Creates first samlpe at random.
    sample_list.append(random.choice(list(corpus.keys())))

    # Populaates sample_list with n items.
    for i in range(n):
        link_list= []
        probability_list = []

        distribution = transition_model(corpus, sample_list[i], damping_factor)
        for i, j in distribution.items():
            link_list.append(i)
            probability_list.append(j)

        sample_list.append(np.random.choice(link_list, p = probability_list))

    rank = copy.deepcopy(corpus)

    # Set up rank key's item == to 0 for later count apparence in sample_list.
    for key in rank:
        rank[key] = 0

    # Counts how many copies of each page(key) there are in the samples.
    for key in sample_list:
        rank[key] += 1

    # Converts count of apperance in probability.
    for key in rank:
        rank[key] = rank[key] / n

    return rank

    raise NotImplementedError


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    rank = copy.deepcopy(corpus)
    treshold = 0.001
    avg_displacement = treshold + 1

    #sets initial rank of all pages to 1/N.
    for page in rank:
        rank[page] = 1 / len(corpus)

    # Calculates PageRank until treshold is met.
    while avg_displacement > treshold:
        past_rank = copy.deepcopy(rank)
        displacement = copy.deepcopy(corpus) # Will contain absolute value of displacement of probability  for each page.
        sum = 0 

        # iterates through corpus to calculate PR(p).
        for page in corpus:
            sigma_ratio = 0

            # Iterates thtough corpus to find keys(pages) where page(p) is a link to calculate the sum of ratios (PR(i) / NumLinks(i)).
            for key, link_list in corpus.items():
                if page != key:
                    if len(link_list) != 0:
                        for link in link_list:
                            if page == link:
                                sigma_ratio += rank[key] / len(link_list)
                    else:
                        sigma_ratio += rank[key] / len(corpus)

            rank[page] = ((1 - damping_factor) / len(corpus)) + (damping_factor * sigma_ratio)

        # Calculates displacement of probability for every page in corpus for later use calculating avg displacement.
        for page in past_rank:
            displacement[page] = abs(rank[page] - past_rank[page])
            sum += displacement[page]

        avg_displacement = sum / len(corpus)        

    return rank
    

    raise NotImplementedError

if __name__ == "__main__":
    main()

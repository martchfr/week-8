from collections import defaultdict
import re
import numpy as np
import pandas as pd


class MarkovText(object):

    def __init__(self, corpus):
        self.corpus = corpus
        self.term_dict = None  # you'll need to build this

    def get_term_dict(self):
        """Builds and returns a dictionary mapping each term to its possible next terms."""
        
        # Initalizes the object property of self as a dictionary of lists.
        self.term_dict = {}

        # Manipulate the corpus into two components: (1) a list of all terms and (2) a list of unique terms.
        self.corpus = re.sub(r'[^\w\s]','',self.corpus) # Remove all punctuation
        corpus_terms = self.corpus.split(' ') # Split corpus into a list of terms
        corpus_terms = [x for x in corpus_terms if x] # Remove empty strings
        corpus_terms_dict = list(dict.fromkeys(corpus_terms)) # Get list of unique terms

        # Setup a PD Dataframe to hold all of the terms and their positions
        corpus_df = pd.DataFrame({"First Term": corpus_terms}) # Setup dataframe
        corpus_df["Next Term"] = corpus_df["First Term"].shift(-1) # Get next term
        corpus_df[corpus_df['First Term'] == 'comes']

        # Loop through unique terms and populate the term_dict with possible next terms
        for term in corpus_terms_dict:
            corpus_df[corpus_df['First Term'] == term]
            self.term_dict[term] = (
                corpus_df[corpus_df['First Term'] == term]['Next Term']
                            .tolist()
            )

        return self.term_dict


    def generate(self, seed_term=None, term_count=15):
        """Generates and returns a sequence of terms based on the Markov model and user input on seed_term and term_count."""

        #If seed_term is not provided, randomly select one from the term_dictionary.
        if seed_term is None:
            seed_term = np.random.choice(list(self.term_dict.keys()))
        elif seed_term not in self.term_dict:
            raise ValueError(f"Seed term '{seed_term}' not found in term dictionary.")

        # Define term sequence list and initialize with seed_term.
        term_sequence = [seed_term]

        # Iterate through the term_count to build the sequence of terms.
        for i in range(term_count - 1):
            next_term = np.random.choice(self.term_dict[seed_term])
            term_sequence.append(next_term)
            seed_term = next_term

        return term_sequence

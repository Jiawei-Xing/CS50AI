import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def pass_one_gene(n):
    if n == 0:
        p = PROBS["mutation"]
    elif n == 1:
        p = 0.5 * (1 - PROBS["mutation"]) + 0.5 * PROBS["mutation"]
    elif n == 2:
        p = 1- PROBS["mutation"]
    return p


def pass_no_gene(n):
    if n == 0:
        p = 1- PROBS["mutation"]
    elif n == 1:
        p = 0.5 * (1 - PROBS["mutation"]) + 0.5 * PROBS["mutation"]
    elif n == 2:
        p = PROBS["mutation"]
    return p


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    p = 1
    for person in people:

        # mother
        m = people[person]["mother"]
        if m in one_gene:
            m_gene = 1
        elif m in two_genes:
            m_gene = 2
        else:
            m_gene = 0

        # father
        f = people[person]["father"]
        if f in one_gene:
            f_gene = 1
        elif f in two_genes:
            f_gene = 2
        else:
            f_gene = 0

        # one gene
        if person in one_gene:
            n_gene = 1
            if m == None and f == None:
                p *= PROBS["gene"][1]
            else:
                p *= pass_one_gene(m_gene) * pass_no_gene(f_gene) + \
                     pass_one_gene(f_gene) * pass_no_gene(m_gene)

        # two genes
        elif person in two_genes:
            n_gene = 2
            if m == None and f == None:
                p *= PROBS["gene"][2]
            else:
                p *= pass_one_gene(m_gene) * pass_one_gene(f_gene)

        # no gene
        else:
            n_gene = 0
            if m == None and f == None:
                p *= PROBS["gene"][0]
            else:
                p *= pass_no_gene(m_gene) * pass_no_gene(f_gene)

        # trait
        if person in have_trait:
            p *= PROBS["trait"][n_gene][True]
        else:
            p *= PROBS["trait"][n_gene][False]
    return p


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        if person in one_gene:
            probabilities[person]["gene"][1] += p
        elif person in two_genes:
            probabilities[person]["gene"][2] += p
        else:
            probabilities[person]["gene"][0] += p

        if person in have_trait:
            probabilities[person]["trait"][True] += p
        else:
            probabilities[person]["trait"][False] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        s = probabilities[person]["gene"][0] + probabilities[person]["gene"][1] + probabilities[person]["gene"][2]
        probabilities[person]["gene"][0] /= s
        probabilities[person]["gene"][1] /= s
        probabilities[person]["gene"][2] /= s

        t = probabilities[person]["trait"][True] + probabilities[person]["trait"][False]
        probabilities[person]["trait"][True] /= t
        probabilities[person]["trait"][False] /= t


if __name__ == "__main__":
    main()

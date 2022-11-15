# Candidate key calculator

Finds the candidate key(s) in a given relation.

 # Input
 * The relational schema in the form `A, B, C, D`.
 * The functional dependencies over the relation schema in the form `A->B, B->C, D->C`.
___
# Known limitations
* Doesn't account for functional dependencies that have the exact same attribute(s) on the left side. So an input like `C->D, C->B, A->E` will not work.
Therefore, the input should instead be `C->DB, A->E`.
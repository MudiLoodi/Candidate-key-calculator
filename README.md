# Functional Dependency Analyzer

This script is a tool for analyzing functional dependencies in relational databases.


Categorizes attributes based on their role in dependencies:
* Left side only (determinants)
* Right side only (dependents)
* Both sides
* Neither side

then finds candidate keys (minimal sets of attributes that uniquely determine all other attributes).

#### Use Case:
* Database design and normalization
* Understanding data dependencies
* Identifying primary keys
* Teaching/learning relational database theory

### Input
 * The relational schema in the form `A, B, C, D`.
 * The functional dependencies over the relation schema in the form `A->B, B->C, D->C`.
___
### Known limitations
* Doesn't account for functional dependencies that have the exact same attribute(s) on the left side. So an input like `C->D, C->B, A->E` will not work.
Therefore, the input should instead be `C->DB, A->E`.

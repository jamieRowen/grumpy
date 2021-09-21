## grumpy_checks 0.1.7 _2021-09-22_

    * Added checks for documentation
    * Added scripts to generate 
        * codecov report
        * documetation html
        * run tests
    * Added a bunch of test cases for lint and news
    * Fixed all warnings issues that grumpy raises on itself

## grumpy_checks 0.1.6 _2021-09-18_

    * Renamed due to existing use of `grumpy` on pypi.org
    * Manually published to pypi this version

## grumpy 0.1.4 _2021-09-18_

    * Redesign interface
        * All checks return a CheckResponse
        * A category of check functions is a CheckCollection
        * A group of categories is a CheckCollectionGroup
    * Redesigned interface makes it easier to extend individual groups with
    new checks
    * Also made it easier to make consistent behaviour when running either
    a category or a group
    * Made it easier to create log output consistently
    * Simple logging mechanism added

## grumpy 0.1.3 _2021-09-17_

    * Update README
    * Some improvements to the CLI

## grumpy 0.1.2 _2021-09-17_

    * Start adding in some CLI via cleo

## grumpy 0.1.1 _2021-09-16_

    * Add some initial news file checks
        * check NEWS.md exists
        * check NEWS.md version matches toml version
        * check NEWS.md has correct format

## grumpy 0.1.0 _2021-09-16_

    * Intial commit
    * Add skeleton functionality for checks with reporting
    * Add skeleton functionality for register plugin style checks
    * Add some initial lint checks
        * flake8 file exists
        * run flake8
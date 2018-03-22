# ACS_Summary_File

Originally this suite of programs was to create a specific extract from the ACS Summary Files. All of the early programs were in a combination of bash and awk scripts. 

The revised set of programs will be written in python where possible for more efficient code (and as a python learning experience).

Current goals are the following:

1. Remove dependency on shell scripts to provide python3 only solution (nearing completion)

2. Allow user specified year and period for the source dataset. (done)

3. Allow specification of table ids and summary level. Ideally also include ability to use wildcards. (Only startswith capability so far)

4. Either dynamically pull down the necessary datasets or use locally cached files based on availability. (done)

5. Unzip the files from within python (done)

6. Assemble the datasets into a useful form (todo)

7. In the long-term, create a useful enough program to share broadly. (not yet!)

# AUCR Change Log

## AUCR Release 0.7.3

-  Add codacy reporting badge to the Readme.md
-  Fix Markdown formatting issues in Markdown documents. 

## AUCR Release 0.6.1.3

-  Fix error code handling so in the case of a failure when it doesn't find an error code it's looking for it defaults to http error code 500
-  FINALLY Fix the default / page request to return the login page and not return a 404 error
-  Fix a bug found by Nicholas Taylor if you submitted fields to login but didn't fill them all out it would return a broken page with the values showing up as the labels
 
## AUCR Release 0.6.1.2

Thanks to Nicholas Taylor for the bug report
-  Fix issue #71 to not fail if ES takes to long to response to a index/search/delete request

Starting with release v 0.6.0.0 we will document all changes in minor/major releases 

## AUCR Release 0.6.0.0


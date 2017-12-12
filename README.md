Hackster
========
Block for pulling information about projects or products from Hackster.io.  Uses client only authentication.

Properties
----------
- **creds**: Client ID and Client Secret from your Hackster application
- **endpoint**: Either projects or products depending what information you want to get.
- **include_query**: Whether to include queries in request to Hackster.
- **polling_interval**: How often Hackster is polled. When using more than one query. Each query will be polled at a period equal to the *polling interval* times the number of queries.
- **queries**: Inherited from base rest polling block but not used. Any random string should be entered in the field.
- **retry_interval**: When a url request fails, how long to wait before attempting to try again.
- **retry_limit**: Max number of times to retry on a poll.

Inputs
------
- **default**: Any list of signals.

Outputs
-------
- **default**: Query results from Hackster sent as a list of signals.

Commands
--------
None

Dependencies
------------
None


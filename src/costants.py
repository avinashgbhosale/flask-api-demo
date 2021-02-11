# - coding: utf-8 --

# CODE	STATUS	FIELD	DESCRIPTION
# 401	NOT_AUTHORIZED	null	Invalid token or user not authenticated
# 400	INVALID_FIELD	“field_name”	Missing or invalid field
# 400	INVALID_SERVICE	null	Service ID mentioned in path does not belong to said Event
# 404	NOT_FOUND	null	Event or Service not found
# 403	PERMISSION_DENIED	null	User role not allowed to perform such action
# 500	SERVER_ERROR	null	Internal server error


DATE_YMD_FORMAT = "%Y-%m-%d"

GITHUB_USER_SEARCH_URL = "https://api.github.com/search/users"
GITHUB_REPOS_BY_USER_URL = "https://api.github.com/users/{}/repos"

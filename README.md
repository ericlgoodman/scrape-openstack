# scrape_openstack

Ask Openstack is a forum similar to StackOverflow but made specifically for Openstack users. Topics can be sorted by recent activity, number of votes, but not by the number of views they have received. To gather data on common user problems, this script scrapes every page and maps each question to the number of views it has received. It then sorts the data, throwing away any topics with fewer than 100 views, and writes the output to a simple Excel file.

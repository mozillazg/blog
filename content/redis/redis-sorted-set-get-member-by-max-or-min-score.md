

http://stackoverflow.com/questions/20017255/how-to-get-a-member-with-maximum-or-minimum-score-from-redis-sorted-set-given

Member with minimum score:

ZRANGEBYSCORE myset -inf +inf WITHSCORES LIMIT 0 1

Member with maximum score:

ZREVRANGEBYSCORE myset +inf -inf WITHSCORES LIMIT 0 1
docker exec -t db_postgres pg_dumpall -c -U username > $HOME/git/flavor_forest/postgres/dump.sql

test
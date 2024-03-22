# src/db

This directory is mounted to `/docker-entrypoint-initdb.d` in the database
container. Any SQL files in this directory will be run when the database starts
for the first time.

For more information, see **Initialization Scripts** on the PostgreSQL Docker
Hub site: [postgres](https://hub.docker.com/_/postgres)

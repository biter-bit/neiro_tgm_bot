#!/bin/bash

export PGPASSWORD='postgres'
script_dir=$(dirname "$0")

#psql -h db_new -U postgres -d sqlalchemy_tuts -f "$script_dir/fixtures/tariff.sql"
#psql -h db_new -U postgres -d sqlalchemy_tuts -f "$script_dir/fixtures/ai_model.sql"
psql -h localhost -U postgres -d sqlalchemy_tuts -f "$script_dir/fixtures/tariff.sql"
psql -h localhost -U postgres -d sqlalchemy_tuts -f "$script_dir/fixtures/ai_model.sql"

unset PGPASSWORD

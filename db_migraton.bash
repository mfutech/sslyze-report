#!/bin/bash
#
#

BASEDIR=$(dirname $0)
CONFIG_FILE=${BASEDIR}/config.ini
MIGRATION_DIR=${BASEDIR}/db_migration
DB_FILE=$(awk -F "= " '/db_path/{print $2}' $CONFIG_FILE)

echo "BASEDIR: $BASEDIR"
echo "CONFIG_FILE: $CONFIG_FILE"
echo "BD_FILE: $DB_FILE"
echo "MIGRATION_DIR $MIGRATION_DIR"

cd $BASEDIR

if [ -z "$DB_FILE" ]; then
  echo "db file configuration not found... exit"
  exit -1
fi

if [ ! -f "$DB_FILE" ]; then
    touch $DB_FILE
fi

for f in $(ls ${MIGRATION_DIR}/*.sql); do
  echo "processing $f"
  sqlite3 $DB_FILE < $f
done
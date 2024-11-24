#!/bin/bash

CFG_DIR=./eos-configs

configure_HOST() {
  docker cp $CFG_DIR/$1.sh clab-ceos-evpn-clos2-$1:/tmp/
  docker exec clab-ceos-evpn-clos2-$1 bash /tmp/$1.sh 2>/dev/null
}

echo
PIDS=""
HOST=("host1" "host2" "host3" "host4")

for VARIANT in ${HOST[@]}; do
  ( configure_HOST $VARIANT ) &
  REF=$!
  echo "[$REF] Configuring $VARIANT..."
  PIDS+=" $REF"
done

echo
for p in $PIDS; do
  if wait $p; then
    echo "Process $p success"
  else
    echo "Process $p fail"
  fi
done
echo
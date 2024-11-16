#!/bin/bash

# Wait for Pinot Controller to be ready
echo "Waiting for Pinot Controller to be ready..."
until curl -s http://pinot-controller:9000/health > /dev/null; do
    echo "Pinot Controller is not ready yet..."
    sleep 5
done

echo "Adding schema..."
curl -X POST -H "Content-Type: application/json" -d @/opt/pinot/config/schema.json http://pinot-controller:9000/schemas

echo "Waiting for schema to be added..."
sleep 5

echo "Adding table config..."
curl -X POST -H "Content-Type: application/json" -d @/opt/pinot/config/table.json http://pinot-controller:9000/tables

echo "Pinot setup completed!"
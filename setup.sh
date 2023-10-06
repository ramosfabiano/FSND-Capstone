#!/bin/bash

# database
export DATABASE_URL="postgresql://postgres:1234@localhost:5432/fsnd_capstone"

# authentication
export ENABLE_AUTH=1
export AUTH0_DOMAIN="dev-rvbtc77b8udvaibw.us.auth0.com" 
export ALGORITHMS="RS256"
export API_AUDIENCE="fsnd-capstone" 

# for submission purposes
export AUTH0_CLIENT_ID="GnZ9oyet4BRVLgbXc17klkbGVOsKRX81"
export AUTH0_CLIENT_SECRET="l2PLVxrfo6YLodEmu3XCIkuyLLxs5e4HQsxYl0qDYHLzUeLd5IL3XMSFouf2pAHl"
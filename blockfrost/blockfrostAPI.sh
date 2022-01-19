# usage => bash ./blockfrostAPI.sh

# get info about address
cmd=$(curl -H 'project_id: {API Key}' https://cardano-mainnet.blockfrost.io/api/v0/addresses/{address})

echo $cmd
async function createWallet() {
  const res = await fetch('/create-wallet')
  const wallet = await res.json()
  document.getElementById('wallet').textContent = JSON.stringify(wallet, null, 2)
}

async function sendTransaction() {
  const sender = document.getElementById('from').value
  const recipient = document.getElementById('to').value
  const amount = parseFloat(document.getElementById('amount').value)
  const res = await fetch('/send', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ sender, recipient, amount })
  })
  const result = await res.json()
  document.getElementById('output').textContent = JSON.stringify(result, null, 2)
}

async function mine() {
  const miner = document.getElementById('from').value
  const res = await fetch('/mine', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ miner_address: miner })
  })
  const result = await res.json()
  document.getElementById('output').textContent = JSON.stringify(result, null, 2)
}

async function loadChain() {
  const res = await fetch('/chain')
  const chain = await res.json()
  document.getElementById('output').textContent = JSON.stringify(chain, null, 2)
}


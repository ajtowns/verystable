#!/usr/bin/env python3

import sys
import verystable.script as script

# Usage:
#   cat txhex | examples/dotgraph.py | dot -Tpng > txhex.png
# then view txhex.png

def human_btc(amt):
    if amt > 10000000:
        return "%d.%08d BTC" % (amt//100_000_000, amt%100_000_000)
    elif amt > 100000:
        return "%d.%05d mBTC" % (amt//100_000, amt%100_000_000)
    else:
        return "%d.%02d uBTC" % (amt//100, amt%100) # bits rule, sats drool

def main(f):
    ## read the txid info
    txids = {}
    for line in f:
        tx = script.CTransaction.fromhex(line.strip())
        txid = tx.rehash()
        spends = [("%32x" % inp.prevout.hash, inp.prevout.n) for inp in tx.vin]
        outs = [out.nValue for out in tx.vout]
        txids[txid] = spends, outs

    ## convert into graphviz
    print("digraph {")
    for txid, (spends, out) in txids.items():
        for txid_in,n in spends:
            if txid_in in txids:
                value = human_btc(txids[txid_in][1][n])
            else:
                value = "?"
                continue
            print('  "%s" -> "%s" [label="%d:%s"]' % (txid_in, txid, n, value))
    print("}")

if __name__ == "__main__":
    main(sys.stdin)

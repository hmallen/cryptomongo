# CryptoMongo

Dump trade data from Cryptowat.ch websockets into MongoDB via PyMongo. Rough and quickly assembled for use with another project with real-time trade flow analysis at the core.

From MongoDB, chart with the new Mongo charting tools, create some plots with Plot.ly, matplotlib, etc. Perhaps some technical analysis with TA-Lib? Wanna get fancy with an Elastic Stack? The world...er, database...is your oyster!

## To Do

* Implement better guarantees for near 100% uptime
  * Multi-node ingestion pipeline (Kafka or similar)
  * Redundant websocket inputs (Probably too costly in terms of bandwidth, etc.)
  * Optimize exception handling for rapid restoration of failed websockets connection
* Strip down/simplify output variables presented and stored in db.
* Add some real time analysis tools to observe rates of change price and related metrics
* Add orderbook and/or spread tracking functions
* Create utility librar(y/ies) for offline or post-hoc historical data analysis
* Begin evaluating potential for analytical approaches that consistently yield valid predictive models (short and long term)
* Test some direct data acquisition directly from exchange to determine timing differences in data arrival
  * Add exchange websockets if difference is significant

## Notes

* Testing data acquisition from 15 high volume markets simultaneously didn't show any issues with reliable database storage
* If overload occurs, can easily implement Apache Kafka as stream buffering mechanism

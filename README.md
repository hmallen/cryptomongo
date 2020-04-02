# mongotrades

Dump trade data from Cryptowat.ch websockets into MongoDB via PyMongo. Rough and quickly assembled for use with another project.

## Notes

* Testing with 15 medium to high volume markets didn't show any issues with buffering when saving to db
* If overload occurs, can easily implement Apache Kafka as stream buffering mechanism

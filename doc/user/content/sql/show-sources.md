---
title: "SHOW SOURCES"
description: "`SHOW SOURCES` returns a list of all sources available in Materialize."
menu:
  main:
    parent: commands
---

`SHOW SOURCES` returns a list of all sources available in Materialize.

## Syntax

{{< diagram "show-sources.svg" >}}

Field | Use
------|-----
_schema&lowbar;name_ | The schema to show sources from. Defaults to first resolvable schema in the search path. For available schemas, see [`SHOW SCHEMAS`](../show-schemas).
_cluster&lowbar;name_ | The cluster to show sources from. If omitted, sources from all clusters are shown. For available clusters, see [`SHOW CLUSTERS`](../show-clusters).

## Details

### Output format for `SHOW SOURCES`

`SHOW SOURCES`'s output is a table, with this structure:

```nofmt
name  | type | cluster
------+------+--------
...   | ...  | ...
```

Field | Meaning
------|--------
**name** | The name of the source.
**type** | The type of the source: `kafka`, `postgres`, `load-generator`, `progress`, or `subsource`.
**cluster** | The cluster the source is associated with.

## Examples

```mzsql
SHOW SOURCES;
```
```nofmt
            name    | type     | cluster
--------------------+----------+---------
 my_kafka_source    | kafka    | c1
 my_postgres_source | postgres | c2
```

```mzsql
SHOW SOURCES IN CLUSTER c2;
```
```nofmt
name               | type     | cluster
-------------------+----------+--------
my_postgres_source | postgres | c2
```

## Related pages

- [`CREATE SOURCE`](../create-source)
- [`DROP SOURCE`](../drop-source)
- [`SHOW CREATE SOURCE`](../show-create-source)

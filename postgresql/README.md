# PostgreSQL Cheat Sheet

* [Reference](https://www.postgresql.org/docs/current/bookindex.html)
* [JSON](https://www.postgresql.org/docs/current/functions-json.html)
* [PL/pgSQL](https://www.postgresql.org/docs/current/plpgsql.html)
* [6 Simple and Useful Features](https://it.badykov.com/blog/2022/09/12/simple-and-usefull-postgresql-features/)
    * `INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY`
    * `COALESCE(NULLIF())`
    * `GROUP BY GROUPING SETS/ROLLUP/CUBE`
    * `WITH name (columns) AS (crud_query) main_query`
    * `CREATE DOMAIN alias long_type`
    * `JOIN table USING (a, b, c)`

## How to select min/max with `DISTINCT ON`

* [Docs](https://www.postgresql.org/docs/current/sql-select.html#SQL-DISTINCT)

* Without `DISTINCT ON`:

```sql
SELECT "location", "time", "report"
FROM "weather_reports"
ORDER BY "location", "time";
```

|location|time|report|
|--------|----|------|
|L1|T1|R1|
|L1|T2|R2|
|L1|T3|R3|
|L2|T4|R4|
|L2|T5|R5|

* Select min `time` per `location`:

```sql
SELECT DISTINCT ON ("location")
    "location", "time", "report"
FROM "weather_reports"
ORDER BY "location", "time";
```

|location|time|report|
|--------|----|------|
|L1|T1|R1|
|L2|T4|R4|

* Select max `time` per `location`:

```sql
...
ORDER BY "location", "time" DESC;
```

## Data migration from single JSON to multiple tables

```sql
WITH
    "treeInserted" AS (
        INSERT INTO "public"."tree" ("itemId", "createdAt", "dataBySimplePath")
            SELECT
                "item"."id",
                "tree"."createdAt",
                "tree"."data" #>> '{by,simple,path}'
            FROM "public"."item" AS "item"
                CROSS JOIN jsonb_to_recordset("item"."trees")
                    AS "tree" (
                        "createdAt" timestamptz,
                        "data" jsonb
                    )
            WHERE "item"."trees" IS NOT NULL
        RETURNING *
    ),
    "branchInserted" AS (
        INSERT INTO "public"."branch" ("treeId", "key", "foo", "bar")
            SELECT
                "treeInserted"."id",
                "branch"."key",
                "branch"."value" -> 'foo',
                "branch"."value" -> 'bar'
            FROM "treeInserted"
                INNER JOIN "public"."item" AS "item"
                    ON "treeInserted"."itemId" = "item"."id"
                INNER JOIN jsonb_to_recordset("item"."trees")
                    AS "tree" (
                        "createdAt" timestamptz,
                        "data" jsonb
                    )
                    ON "treeInserted"."createdAt" = "tree"."createdAt"
                CROSS JOIN jsonb_each("tree"."data" -> 'branches') AS "branch"
        RETURNING *
    ),
    "leafInserted" AS (
        INSERT INTO "public"."leaf" ("branchId", "baz")
            SELECT
                "branchInserted"."id",
                "leaf"."baz"
            FROM "branchInserted"
                INNER JOIN "treeInserted"
                    ON "branchInserted"."treeId" = "treeInserted"."id"
                INNER JOIN "public"."item" AS "item"
                    ON "treeInserted"."itemId" = "item"."id"
                INNER JOIN jsonb_to_recordset("item"."trees")
                    AS "tree" (
                        "createdAt" timestamptz,
                        "data" jsonb
                    )
                    ON "treeInserted"."createdAt" = "tree"."createdAt"
                INNER JOIN jsonb_each("tree"."data" -> 'branches') AS "branch"
                    ON "branchInserted"."key" = "branch"."key"
                CROSS JOIN jsonb_to_recordset("branch"."value" -> 'leafs')
                    AS "leaf" (
                        "baz" text
                    )
    )
SELECT 'JSON data migration' AS "done";
```

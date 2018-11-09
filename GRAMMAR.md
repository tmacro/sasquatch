# multitool Verbs
Verbs are shown in the following format:
```
verb:<required argument>:[optional arguement]
```
Verbs  can be chained using `|`
```
List all versions in all buckets and count them: ls|ls|count
```
Required and optional arguments can be passed from the preceding Verb
This lists all objects in `mybucket` then pass the bucket & key to `lv` to list all versions of that object
```
ls:mybucket|lv
```

## Listing
List objects from storage
```
ls:[bucket]
```
List buckets or objects if `bucket` provided

```
lv:<bucket>:[key]
```
List object versions

```
lr:[bucket]
```
List all CRRs or CRRs scoped by bucket

## Operations
Perform operations on objects
```
head:<bucket>:<key>:[version-id]
```
HEAD an object

```
get:<bucket>:<key>:[versionid]
```
GET and object

```
put:<bucket>:[key]:[file=/path/to/file]:[content=[zero,rand]]:[size=100B]
```
PUT object in bucket at key

```
mpu:<bucket>:[key]:<parts=10>:[content=[zero,rand]]
```
Similar to `put` this uploads an object as an mpu using `parts` object parts

## Filter
Filter lists of objects or buckets
Filters can be negated by adding a `!`  as its first argument
eg `gr:!:rejecthispattern`
```
gr:<regex>
gr:<regex>
```
Match names based on a regex

```
rstat:<status>
```
Filter based upon replication status

```
all
```
Match everything

## Stats
Generate counts based upon filters, these will be printed at the end of the run
Optionally these can take a `label` which will be printed along with the count
```
stat:<filter>:[label]
```
Counts emitted items based upon filter
`stat:gr:^matchthisline$`

```
count:[label]
```
Special filter that behaves like `stat:all`. Simply count all items

## Generators
Create resources
All generators use uuid4 to create unique names if no `prefix` is given
```
bkt:<count>:[prefix]
```
Generate `count` buckets beginning with `prefix` if given

```
obj:<count>:[prefix]
```
Generate `count` objects beginning with `prefix` if given

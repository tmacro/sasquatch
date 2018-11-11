
#  General Syntax



sq consists of two principle symbols `Verbs` and `Nouns`.
Sets of `Verbs` and `Nouns` can be chained together to form `Clauses`.
Data flows from left to right with the output of one `Verb` becoming the input for the next.

## Verbs

`Verbs` are analogous to functions with `Nouns` being their arguments.



```

	head			# An example Verb

	ls:mybucket 		# Verb with Noun

	get:mybucket:myobject	# Verb with two Nouns

```

More than one `Verb`  can be chained together using pipe `|` into a `Clause`.
The output of each `Verb` becomes the `Nouns` for the next `Verb` in the chain, allowing complex behavior to be built.

```

	# List a bucket and HEAD each object
	ls:mybucket | head

	# Copy only media files from one bucket to another
	ls:mymedia | gr:.*\.mp4$ | cp:mymp4s

	# Count the number of object successfully replicated
	lr:mycrrbucket | rstat:SUCCESS | count

```

## Nouns

`Nouns` come in two flavors, **positional** and **keyword**, however all `Nouns` have any associated keyword.
Internally all positional `Nouns` are mapped to  keywords for identification, as such positional `Nouns` can be thought of as a less verbose form of keyword `Nouns`  that are provided to the user for convenience.

```

	# this
	ls:mybucket:myobject

	# is the same as this
	ls:bucket=mybucket:key=myobject

```

Not all `Nouns` can be specified as positional for every `Verb`.  Consult the Language Reference for more details

# Language Reference

## Available  Verbs

`Verbs` are shown in the following format:  `verb:<required argument>:[optional arguement]`


##  Listing

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



##  Operations

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



##  Filter

Filter lists of objects or buckets

Filters can be negated by adding a `!` as its first argument

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



##  Stats

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



##  Generators

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

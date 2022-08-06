# Structured Sort

ssort (structured sort) is a tool for sorting yaml and json files in a configurable way.

# Example

Input:

```yaml
meta:
  name: contacts
  version: 1.0.0
  description: Contacts
list:
- firstname: John
  lastname: Doe
  contact:
    mobile: "12345678"
    telephone: "987654321"
- lastname: Smith
  firstname: Jane
  contact:
    mobile: "87654321"
    email: jane.smith@gmail.com
    telephone: "12345678"
- firstname: Edgar
  lastname: Poe
  somemore: dont care about this
  contact:
    mobile: "12345678"
    email: poe@gmail.com
  secondname: Allan
  other: not important
```

Sorting Definition:

```yaml
meta:
  sort: 
    by: none
list:
  sort:
    by: element
    value: firstname
  each:
    sort:
      by: custom
      order:
      - firstname
      - secondname
      - lastname
      - contact
    contact:
      sort: 
        by: key
```

Output:

```yaml
meta:
  name: contacts
  version: 1.0.0
  description: Contacts
list:
- firstname: Edgar
  secondname: Allan
  lastname: Poe
  contact:
    email: poe@gmail.com
    mobile: '12345678'
  somemore: dont care about this
  other: not important
- firstname: Jane
  lastname: Smith
  contact:
    email: jane.smith@gmail.com
    mobile: '87654321'
    telephone: '12345678'
- firstname: John
  lastname: Doe
  contact:
    mobile: '12345678'
    telephone: '987654321'
```

# Writing a Sorting Definition

## Stucture
Sorting definitions are structured in the same way as the file to be sorted. You can think of the base file as a tree, where the root is the top level of the file, and the children are the elements. Each tree element can define how to sort its children. To achieve this ssort defines the sorting keyword "sort" and ways to reference the children of an element.

## Sort Keyword
The sort keyword defines how to sort the children of an element.

Example:

```yaml
sort: 
  by: key
```
There are five options to sort by.

### No Sort
```yaml
sort: 
  by: none
#or
sort: none
```
This option will not sort the children. Note that this is the default option.

### Sort by Key

```yaml
sort: 
  by: key
#or 
sort: key
```
Sorts the children of an element alphabetically by key ignoring case. If the element is a list of primitives, they are sorted alphabetically by their string representation.

### Sort by Value

```yaml
sort: 
  by: value
#or
sort: value
```
If the element is a list of primitives, they are sorted alphabetically by their string representation.
If the element is a map, and all values are primitives, the map is sorted alphabetically by the string representation of the values.

### Sort by Element

```yaml
sort: 
  by: element
  value: <value>
#or
sort: element.<value>
```
Sorts all the children of the element that have a child calle <value> by the value of that child. All other children are at the end of the list.

### Sort by Custom Order

```yaml
sort: 
  by: custom
  order:
  - <value>
  - <value>
  - <value>
  - <value>
#or
sort:
- <value>
- <value>
- <value>
- <value>
```
Sorts the children of an element by the order of the values in the order list. All other children are at the end of the list in the order they appeared in originally.

## Referencing Children

To sort multiple levels of children in the document, you can reference the children of an element.

Example:

```yaml
each:
  sort: key
```

There are three ways of referencing children.

### By Key

```yaml
<key>:
```
This references the child with the key <key>.

Example:

Input
```yaml
meta:
  name: example
info:
  version: 1.0.0
  description: Example
content:
  - 2
  - 1
  - 3
  - 4
```
Sort Definition:

```yaml
#reference by key
content:
  #value sort
  sort: value
```
Output:
```yaml
meta:
  name: example
info:
  version: 1.0.0
  description: Example
content:
  - 1
  - 2
  - 3
  - 4
```

### Each
This references all children of the element.

```yaml
each:
```

### All
This references all children of the element and all of their children recursively.

```yaml
all:
```

Example:

This sorting definition would sort the whole file alphabetically by key.
```yaml
#sorts the root
sort: key
#sorts all children of the root recursively
all:
  sort: key
```
### Referencing Children multiple times

If the same child of an element is referenced multiple times, the sorting is applied in the following order:
1. The "all" reference
2. The "each" reference
3. A speficic reference by key

Example:


```yaml
sort: key
all:
  sort: key
each:
  sort: 
    - summary
people:
  sort: element.firstname
```
Would sort the whole file alphabetically by key. Then put the "summary" element at the top of each child of the document root. Then sort the "people" element alphabetically by the the first name of each person.










        
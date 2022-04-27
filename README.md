# Markdown2HTML

Welcome! This repository contains a Python (and Ruby) script that processes a Markdown file and converts it to an HTML file with the following formatting. All formatting has to be strict.

## Headings

| Markdown                 | HTML generated             |
| ------------------------ | -------------------------- |
| `# Heading level 1`      | `<h1>Heading level 1</h1>` |
| `## Heading level 2`     | `<h2>Heading level 1</h2>` |
| `### Heading level 3`    | `<h3>Heading level 1</h3>` |
| `#### Heading level 4`   | `<h4>Heading level 1</h4>` |
| `##### Heading level 5`  | `<h5>Heading level 1</h5>` |
| `###### Heading level 6` | `<h6>Heading level 1</h6>` |

## Unordered listing

**Markdown**

```markdown
- Hello
- Bye
```

**HTML generated**

```html
<ul>
  <li>Hello</li>
  <li>Bye</li>
</ul>
```

## Ordered listing

**Markdown**

```markdown
* Hello
* Bye
```

**HTML generated**

```html
<ol>
  <li>Hello</li>
  <li>Bye</li>
</ol>
```

## Text

**Markdown**

```markdown
Hello

I'm a text
with 2 lines
```

**HTML generated**

```html
<p>
  Hello
</p>
<p>
  I'm a text
    <br />
  with 2 lines
</p>
```

## Bold and emphasis text

| Markdown    | HTML generated   |
| ----------- | ---------------- |
| `**Hello**` | `<b>Hello</b>`   |
| `__Hello__` | `<em>Hello</em>` |

## Extra stuff

| Markdown            | HTML generated                     | Description                                        |
| ------------------- | ---------------------------------- | -------------------------------------------------- |
| `[[Hello]]`         | `8b1a9953c4611296a827abf8c47804d7` | convert in MD5 (lowercase) the content             |
| `((Hello Chicago))` | `Hello hiago`                      | remove all `c` (case insensitive) from the content |

## Usage

```bash
$ ./markdown2html.py file.md file.html
```
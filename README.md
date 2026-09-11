# E++ Language Specification

E++ is a programming language designed around one hard rule, namely that every statement is written as a plain English sentence. The only punctuation marks allowed in the language itself are the comma and the period. The program grammar is therefore readable, declarative, and close to ordinary English, while still remaining precise enough for a parser to understand.

Programs written in E++ are saved with the file extension .epp.

## Usage

### Install Python

Make sure Python is installed on your machine before running E++ programs.

```bash
python3 --version
```

If Python is not installed, install it from python.org or your system package manager, then reopen your terminal.

### Running an E++ program from any path

The runner script can be used from any location as long as you pass the full path to the .epp file.

```bash
python /path/to/eppfilerunner.py /path/to/your_program.epp
```

For example:

```bash
python /Users/arvharan/eplusplus/eppfilerunner.py /Users/arvharan/eplusplus/examples/greet.epp
```

You can also run it from inside the project folder like this:

```bash
cd /Users/arvharan/eplusplus
python eppfilerunner.py examples/greet.epp
```

### Example program

```ruby
Begin program.
Let message be the word hello.
Display message.
End program.
```

Save that as greet.epp and run:

```bash
python /Users/arvharan/eplusplus/eppfilerunner.py /Users/arvharan/eplusplus/examples/greet.epp
```

This project includes a simple runner script at eppfilerunner.py and a sample program in the examples folder.

### GitHub and sync

This repository is intended to be synced to GitHub under the repository name arvharan/eplusplus.

```bash
git init
git add .
git commit -m "Initial E++ project setup"
git branch -M main
git remote add origin https://github.com/arvharan/eplusplus.git
git push -u origin main
```

If the repository already exists, skip the git init and remote add steps and just run:

```bash
git add .
git commit -m "Update E++ language files"
git push
```

## 1. Variables

### 1.1 Grammar

A variable is introduced with a sentence in the form below.

```ruby
Let name be the number value.
Let name be the decimal number value.
Let name be the letter value.
Let name be the word value.
Let name be true.
Let name be false.
Let name be the list of the values.
```

A variable may also be updated later with the form below.

```ruby
Set name to value.
Change name to value.
```

### 1.2 Examples

```ruby
Let x be the number 5.
Let user name be the word Alice.
Let letters be the list of the letters a, b, c.
Set x to the number 7.
Change user name to the word Bob.
```

### 1.3 Allowed names

Variable names follow these rules.

- A name is one or more English words.
- Each word begins with a letter.
- After the first letter, the word may continue with letters only.
- Spaces separate words in a multiword name.
- Names are not allowed to match reserved words such as let, set, if, while, repeat, and end.
- Names may be written in lowercase or title case, but the parser normalizes them before checking for reserved words.

### 1.4 Supported value types

- Whole numbers, such as 0, 5, 27.
- Decimal numbers, such as 3.14, 0.5, 10.75.
- Single letters or characters, such as a, z, 7, or space.
- Words or strings, such as hello, Alice, or open door.
- Boolean values, such as true and false.
- Lists, such as the list of the numbers 1, 2, 3, or the list of the words red, green, blue.

### 1.5 Ambiguity and resolution

The main ambiguity is how the parser knows whether a word is a variable name or a keyword. The language resolves this with a simple rule. The parser checks the sentence structure first. If a word sequence appears immediately after let or after a call to set, and it fits the variable-name pattern without punctuation, then it is treated as a variable name. If it matches a reserved word, it is treated as syntax, not a name. Multiword names are allowed only when the sequence is not a keyword phrase and only when it appears in a declaration or assignment slot.

## 2. Statements and Expressions

### 2.1 Grammar

Arithmetic is expressed as normal English sentences.

```ruby
Set total to 4 plus 5.
Set total to 9 minus 2.
Set total to 6 times 7.
Set total to 20 divided by 4.
Set total to 17 remainder 5.
```

Comparisons use complete English phrases.

```ruby
3 is equal to 3.
8 is greater than 5.
2 is less than 9.
5 is not equal to 7.
```

Logical combination uses English words.

```ruby
value and value
value or value
not value
```

### 2.2 Examples

```ruby
Set total to 2 plus 3 times 4.
Set checks to 6 is greater than 3 and 4 is less than 9.
Set flag to not true or false.
Set answer to 10 divided by 2 plus 3.
```

### 2.3 Precedence rule

The parser uses the following precedence order.

1. not
2. times, divided by, remainder
3. plus, minus
4. is equal to, is not equal to, is greater than, is less than
5. and
6. or

When two operators share the same precedence, evaluation proceeds from left to right. This keeps the language readable while still being deterministic. For long expressions that would be confusing, E++ encourages breaking the logic into intermediate variables with a set sentence.

### 2.4 Ambiguity and resolution

The hardest issue is that plain English can be vague. The language resolves this by requiring the operator words to appear in a fixed phrase order and by using precedence. For example, when the parser sees plus and times in the same sentence, it gives times higher priority. This makes a sentence such as 2 plus 3 times 4 parse as 2 plus 12, not 5 times 4. The language also treats is greater than and is less than as comparison operators, not as part of a ruby string.

## 3. Conditionals

### 3.1 Grammar

Conditionals are written as complete sentences and then closed explicitly.

```ruby
If condition.
Then.
Otherwise.
End if.
```

A common form is this.

```ruby
If x is greater than 10.
Set level to the word high.
Otherwise.
Set level to the word low.
End if.
```

### 3.2 Examples

```ruby
If score is greater than 50.
Display the word pass.
End if.

If age is greater than 18 and has ticket is true.
Display the word allowed.
Otherwise.
Display the word denied.
End if.
```

### 3.3 Nested condition example

```ruby
If user age is greater than 18.
If has ticket is true.
Display the word welcome.
End if.
Otherwise.
Display the word sorry.
End if.
```

### 3.4 Ambiguity and resolution

Because the language uses English sentences only, the parser needs a clear block boundary. The solution is a closing sentence, End if., which cannot be mistaken for data or a regular statement. The language does not rely on indentation alone, because indentation is not reliable in all editors and is not strong enough for a parser. Optional commas may appear inside a condition sentence, but they are not required.

## 4. Loops

### 4.1 Grammar

Counted loops are written with a repeat sentence.

```ruby
Repeat number times.
End repeat.
```

Conditional loops use while or until.

```ruby
While condition.
End while.

Until condition.
End until.
```

List iteration uses a for each form.

```ruby
For each item in list.
End for each.
```

Early exit and skip statements are written as ordinary sentences.

```ruby
Stop the loop.
Skip this iteration.
```

### 4.2 Examples

```ruby
Repeat 5 times.
Display the word hello.
End repeat.

While total is less than 100.
Set total to total plus 5.
End while.

Until user name is equal to the word stop.
Read a word into user name.
End until.

For each item in numbers.
Display item.
End for each.

Stop the loop.
Skip this iteration.
```

### 4.3 Ambiguity and resolution

A loop can be ambiguous because the language uses ordinary English and not special brackets. To avoid this, every loop has a clear closing sentence, such as End repeat. or End while. The parser reads until the matching closing marker. The phrase for each item in list is only recognized when it appears in loop-header position, not as a normal sentence about a list value.

## 5. Input and Output

### 5.1 Grammar

Output statements are formed as ordinary English sentences.

```ruby
Display value.
Print value.
Show the value of variable.
```

Input statements store a value directly into a variable.

```ruby
Read a number into variable.
Read a word into variable.
Read a letter into variable.
```

### 5.2 Examples

```ruby
Display the word hello.
Print total.
Show the value of score.
Read a number into age.
Read a word into user name.
Read a letter into first letter.
```

### 5.3 Ambiguity and resolution

The parser distinguishes between showing a literal value and showing a variable by checking whether the sentence says the value of a variable or gives a literal such as the word hello. Input sentences are recognized by the pattern read a type into name. The parser looks for a type word such as number, word, or letter and an identifier in the target slot.

## 6. Functions

### 6.1 Grammar

Function declarations are written as descriptive English sentences.

```ruby
Define a function named name with the parameters parameter name and parameter name.
Define a procedure named name with the parameters parameter name and parameter name.
```

Function bodies end with a closing sentence.

```ruby
End function.
```

A function can return a value with the sentence below.

```ruby
Give back value.
```

Calling a function happens with this pattern.

```ruby
Call name with value and value.
Set result to the result of calling name with value and value.
```

### 6.2 Examples

```ruby
Define a function named add with the parameters left number and right number.
Give back left number plus right number.
End function.

Call add with 3 and 5.
Set total to the result of calling add with 3 and 5.

Define a procedure named greet with the parameter user name.
Display the word hello.
End function.
```

### 6.3 Function with two parameters returning a value

```ruby
Define a function named add bonus with the parameters base value and extra value.
Give back base value plus extra value.
End function.

Repeat 4 times.
Set total to the result of calling add bonus with total and 5.
Display total.
End repeat.
```

### 6.4 Ambiguity and resolution

The biggest challenge is telling a function call apart from a plain sentence. E++ does this by recognizing the call pattern, which starts with call or the phrase result of calling after set. Parameter lists are separated by and, and the function name must be an identifier, not a reserved word. Function declarations are recognized only after define a function named or define a procedure named and are closed with End function.

## 7. Comments

### 7.1 Grammar

Comments are written as ordinary sentences that begin with a human-note marker.

```ruby
Human note, this is only for people.
Comment, this line is not executed.
```

### 7.2 Examples

```ruby
Human note, this loop counts the items in the list.
Comment, the next line reads user input.
```

### 7.3 Ambiguity and resolution

A comment must begin with a special trigger phrase such as human note or comment so the parser can ignore it before execution. This avoids confusion with real executable sentences, even though the rest of the comment is still written in English. The parser removes those lines before parsing the active program.

## 8. Program Structure

### 8.1 Grammar

A complete program has a start and end marker.

```ruby
Begin program.
... statements ...
End program.
```

The language is sentence-oriented rather than line-oriented. Each sentence ends with a period. Line breaks are allowed for readability, but they are not semantic. A program is parsed by sentence boundaries, not by the physical line layout.

### 8.2 Examples

```ruby
Begin program.
Let x be the number 5.
Display x.
End program.
```

### 8.3 Ambiguity and resolution

The parser treats the period as the sentence terminator. This means that commas are allowed inside a sentence and periods end the sentence, while line breaks do not matter. The only special markers are begin program and end program, which are reserved and must appear at the top and bottom of the file.

## 9. Worked Example

The following program is saved as greet.epp.

```ruby
Begin program.
Let user name be the word Alice.
Let score be the number 0.
Read a number into score.
Let total be the number 0.
If score is greater than 0.
Set total to score.
Otherwise.
Set total to 0.
End if.
Define a function named add bonus with the parameters base value and extra value.
Give back base value plus extra value.
End function.
Repeat score times.
Set total to the result of calling add bonus with total and 5.
Display total.
End repeat.
Print the word done.
End program.
```

This program declares variables, reads a number from the user, makes a choice with an if statement, defines a function that returns a value, calls it from a loop, and prints the final result.

## 10. Design Notes

E++ is intentionally strict in a few places because the language has to be both readable and parseable without special punctuation. The biggest trade-off is that natural English is too ambiguous to parse safely in every case, so the language reserves a small set of sentence templates. For example, variable declarations use let, assignments use set, function definitions use define a function named, and loops use repeat, while, until, and for each. This makes the grammar clear, but means the language does not allow arbitrary sentence fragments as statements.

The trickiest part to implement is reliable parsing of free-form English. A parser has to decide whether a phrase is a variable name, a keyword, a literal value, or part of a comparison. The language reduces that risk by using fixed sentence patterns, explicit loop closures, and a defined precedence order. The set of reserved words is also kept intentionally small so that names stay readable while avoiding collisions.

## 11. File Extension

E++ programs are saved with the file extension .epp. This includes the worked example in the examples folder and any project file intended for E++ execution.

## 12. Icon Design

The .epp icon is a rounded square with a deep navy background and a bright white letterform. The center contains a thick, geometric E with the two plus signs of the language name placed as a compact pair to the upper right, suggesting both expression and extension. A subtle cyan accent line appears along the lower edge of the E to hint at readability and program flow. The result is simple, friendly, and unmistakably readable on a desktop or file browser, while the E and plus signs reflect the language identity of sentence-based computation and expressiveness.

An SVG version of the icon is included in the assets folder.

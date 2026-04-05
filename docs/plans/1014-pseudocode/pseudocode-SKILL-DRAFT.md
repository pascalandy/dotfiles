---
name: pseudocode
description: Interpret requirements and business logic written as shorthand quasi-code inside code blocks. Use when a file contains start-shorthand blocks, when the user writes ()=> instructions, when collaborators provide quasi-code or natural language descriptions with typos or wrong terminology, or when asked to "interpret shorthand", "expand pseudocode", or "what does this shorthand mean".
---

# PM Pseudocode

- Write requirements and describe how a solution should behave -- in plain English, inside code blocks. No programming knowledge required.
- A product manager / power user writes intent inside code blocks using `()=>` lines. The code block gives you syntax highlighting and structure so you can read back what you wrote. The agent interprets that intent -- including typos, wrong terminology, mixed-language descriptions, and vague phrasing -- and figures out what you mean.
- This is not about implementation. It's about capturing business logic, requirements, and expected behavior in a format that's precise enough for engineers to act on without clarifying questions.

## Examples

### Validate User Input

```js
// start-shorthand
()=> create function that validates user input
()=> check email format is correct
()=> make sure password is at least 8 characters
()=> return true if valid, false otherwise
// end-shorthand
```

### Data Processing

```python
# start-shorthand
()=> iterate over the users list
()=> for each user, if age is over 18, add to adults list
()=> sort adults by name alphabetically
()=> return the sorted list
# end-shorthand
```

### API Call with Error Handling

```js
// start-shorthand
()=> fetch current weather from API
()=> if the request fails, retry once after 2 seconds
()=> if it still fails, return a default "unavailable" response
()=> save successful response to weather.json file
// end-shorthand
```

### Multi-Step Business Logic

```js
// start-shorthand
()=> check if user is logged in
()=> if not, redirect to login page
()=> if yes, fetch their dashboard data
()=> if the data fetch fails, show an error message with a retry button
()=> otherwise render the dashboard
// end-shorthand
```

### Shorthand Inside an Existing File

The PM can drop shorthand into a file that already has real code. Only the shorthand block gets expanded:

```python
# start-shorthand
()=> create a function that reads all CSV files from a directory
()=> merge them into a single dataframe
()=> drop rows where the email column is empty
()=> save the result as merged_output.csv
# end-shorthand
```

## Writing Tips for PMs

**One intent per line.** Break complex logic into small steps.

```js
// Good -- one step per line
// start-shorthand
()=> validate all required form fields
()=> save the form data to the database
()=> send a confirmation email to the user
()=> redirect to the success page
// end-shorthand

// Bad -- too much in one line
// start-shorthand
()=> validate the form, save to database, send confirmation email, and redirect
// end-shorthand
```

**Name the error cases.** The agent can't guess your business rules.

```js
// start-shorthand
()=> process the payment
()=> if the card is declined, show an error and let them retry
()=> if the amount exceeds their daily limit, suggest splitting the payment
()=> if the cart changed since checkout started, refresh totals and ask to confirm
// end-shorthand
```

## Language block for readability

The language hint gives you syntax highlighting so your shorthand is easy to scan. It signals context, not implementation.

| Block | Good for describing... |
|---|---|
| ` ```js ` | Frontend behavior, UI interactions, API calls |
| ` ```python ` | Data processing, scripts, automation |
| ` ```sql ` | Data queries, database rules |
| ` ```bash ` | CLI workflows, deploy steps |
| ` ```text ` | Anything -- when you don't care about context |

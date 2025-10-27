1.Which issues were the easiest to fix, and which were the hardest? Why?

Easiest Issues
* Unused import - Simply deleted import logging. No logic changes needed.
* PEP 8 spacing - Added two blank lines between functions. Just formatting.
* String formatting - Changed "%s: Added %d" % (...) to f-strings. F-strings are actually simpler to write.
* Removing eval() - Deleted the dangerous eval() line. Bandit flagged it as a security risk, fix was straightforward.

Hardest Issues
* Mutable default argument (logs=[])

The bug: Default arguments are evaluated once at function definition, not at each call
The same list object is shared across ALL function calls
This causes logs to accumulate unexpectedly between calls
Had to change to logs=None then initialize inside: if logs is None: logs = []
Why hard: Requires understanding Python's execution model. The bug isn't obvious - code "works" but behaves mysteriously.

* Bare except clause

Had to replace except: with specific exception types
Required analyzing what could actually go wrong: KeyError for missing items, TypeError for wrong types
except: catches EVERYTHING including system exits (Ctrl+C won't work!)
Why hard: Needed to think about error scenarios and write meaningful messages for each.

* File operations without context manager

Changed from f = open() ... f.close() to with open() as f:
Also had to add exception handling: FileNotFoundError, JSONDecodeError
Added encoding specification: encoding="utf-8"
Why hard: Multiple fixes in one - context manager + error handling + encoding.

* Input validation

Added type checking: isinstance(item, str) and isinstance(qty, int)
Added value validation: reject negative quantities
Why hard: Had to think about what inputs are valid and provide helpful error messages.


2. Did the static analysis tools report any false positives?

Yes - One Debatable Warning at line 44:
    pythondef load_data(file="inventory.json"):
        global stock_data  # ← Pylint flags this as bad practice

Reason:

- Global variables make code harder to test and debug
- Can cause unexpected side effects in large applications
- Violates functional programming principles


3. How would you integrate static analysis tools into your actual software development workflow?

* Local Development: I would integrate Pylint, Flake8, and Bandit directly into my code editor. This provides real-time feedback as I type, allowing me to fix style issues, potential bugs, and security risks immediately. I would also run them locally before committing any code.

* Continuous Integration (CI) Pipeline: I would set up a CI workflow (like GitHub Actions) that automatically runs all three static analysis tools every time code is pushed or a pull request is created. I would configure this workflow to fail the build if any high- or medium-severity issues . This enforces a quality and security standard for the entire team and prevents bad code from being merged.


4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?

Measurable Improvements
* Code Quality Score:
    Before: 4.80/10
    After: 8.38/10
    Improvement: +75% increase
* Security Issues:
    Before: 2 vulnerabilities
    After: 0 vulnerabilities
    Result: Safe for production
* Style Violations:
    Before: 11 issues
    After: 1 minor issue (missing newline)
    Compliance: 91%
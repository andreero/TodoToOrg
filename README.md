# TodoToOrg
Todo.txt to Emacs Org Mode converter

## Usage:

### TODO.txt -> Org mode conversion
`>>> python todo2org.py file1.txt file2.txt`    
  will produce converted Org mode files file1.org and file2.org in the same directory.

### Org mode -> TODO.txt conversion
Same syntax, but with --reverse argument

`>>> python todo2org.py file1.org file2.org --reverse`    
  will produce converted files file1_.txt and file2_.txt

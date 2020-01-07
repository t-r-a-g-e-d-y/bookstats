Little tool for pulling stats from my book log.

Provides basic stats such as:  
Books read by year  
Books read by author  
Count per year  
Count per author  

Includes an interactive mode for printing stats and searching the log by book or author.

Log format is simply:

Title (Author First, Last Middle) (Date Finished)  
Title, Author, and Date are tab (\t) separated

I use vim to edit my book log and include this modeline at the bottom of the log:  
`# vim: set expandtab& ts=8 sts=8 sw=8:`

Example log (excluding modeline):

```
2019
Slaughterhouse-Five	(Vonnegut, Kurt)	(1/3)
Anna Karenina	(Tolstoy, Leo)	(2/8)
War and Peace	(Tolstoy, Leo)	(5/11)
```


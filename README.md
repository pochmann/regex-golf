regex-golf
==========

Optimal solver for [Peter Norvig's regex golf program](http://nbviewer.ipython.org/url/norvig.com/ipython/xkcd1313.ipynb?create=1), which was inspired by [xkcd 1313](http://xkcd.com/1313/), which was likely inspired by [regex.alf.nu](http://regex.alf.nu/).

Peter uses a greedy algorithm to find a set of regex components that together cover
all winners (strings that shall be matched). Starting with no components, he greedily
adds the best-looking component, updates what's left to do, and repeats until done.

My `findregex` replacement does the same, except that at each step, it also explores
what happens when *not* using that best-looking component. This is optimal, in the
sense that it finds a shortest possible regex that's a disjunction of the provided
regex components.

Result and runtime comparison for the two main examples (Star Wars/Trek and presidents):
```
Peter                9 chars  0.57 seconds  ' T|E.P| N'
Optimal              9 chars  0.38 seconds  ' T|E.P|^A'
Peter with pairs     9 chars  0.82 seconds  ' .?T|P.*E'
Optimal with pairs   7 chars  0.69 seconds  ' T|P.*E'

Peter               54 chars  3.37 seconds  'a.a|a..i|j|li|a.t|i..n|bu|oo|n.e|ay.|r.e$|tr|ls|po|v.l'
Optimal             52 chars  1.51 seconds  'j|po|a.a|a..i|bu|ma|ix|ho|li|v.l|ls|a.t|ay.|n.e|r.e$'
Peter with pairs    49 chars  3.64 seconds  'i.*o|o.*o|a.a|.f|bu|n.e|ay.|a.t|j|tr|di|rc|po|v.l'
Optimal with pairs  47 chars  2.80 seconds  'po|i.*o|bu|o.*o|j|a.a|a.t|v.l|r.i|rc|ay.|ma|n.e'
```

In the "with pairs" versions, I added components of the forms `a.*b`, `a.+b` and `a.?b`.  
Peter's (as of Jan 11, 2014) is slower because it repeats checking for matches.

My `findregex` function represents a given problem as a component-to-winners mapping.
The recursive `search` function first reduces the problem. Many components are
useless because they cover a subset of what another covers and aren't shorter.
So they're thrown away. Then, it looks for winners only matched by one component.
As these components are needed anyway, they're used right away. This might make
more components useless, so the two steps are repeated until nothing changes anymore.
After this, every still not covered winner has at least two components that can
cover it, so we can pick the best looking component and try with and without it.

Variables of `findregex` explained:

`winners`:  Strings that must be matched. Abbreviated `w` (single) or `ws` (plural).  
`losers`:   Strings that must not be matched.  
`c and cs`: The regex components (single and plural).  
`covers`:   Dictionary mapping each component to a set of winners it matches.  
`answer`:   Semi-global variable holding the best regex found so far.  
`regex`:    The regex being built (with '|'-prefix for simplicity).

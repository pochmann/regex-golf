"""Further improvements to Peter's program."""

# Components of the form a.*b, a.+b and a.?b help get better results:

def regex_components(winners, losers):
    ...
    pairs = {p for w in winners for p in paaairs(w) if not matches(p, losers)}
    return wholes | parts | pairs

def paaairs(w):
    return {w[i]+'.'+q+b for i in range(len(w)) for b in w[i+1:] for q in '*+?'}

# Pre-compiling the regex components speeds things up a little:

def matches(regex, strings):
    "Return a set of all the strings that are matched by regex."
    r = re.compile(regex)
    return {s for s in strings if r.search(s)}

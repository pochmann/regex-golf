"""See the README for explanations/results."""

def findregex(winners, losers):
    """"Find a regex that matches all winners but no losers (sets of strings)."""

    def search(regex, covers):
        """Recursively build a shortest regex from the components."""

        # Simplify: Throw away useless components and handle forced decisions.
        previous = None
        while covers != previous:
            previous = covers

            # Only keep a set of superior components (throw away those that cover
            # a subset of a superior component and aren't shorter).
            COVERS = {}
            for c in sorted(covers, key=lambda c:(-len(covers[c]), len(c))):
                ws = covers[c]
                if ws and not any(ws<=WS and len(c)>=len(C) for C,WS in COVERS.items()):
                    COVERS[c] = ws
            covers = COVERS

            # For winners covered only by one component, use those needed components now.
            coverers = {}
            for c, ws in covers.items():
                for w in ws:
                    coverers.setdefault(w, []).append(c)
            needed = {cs[0] for cs in coverers.values() if len(cs) == 1}
            if needed:
                regex += '|' + '|'.join(needed)
                covered = {w for c in needed for w in covers[c]}
                covers = {c:ws-covered for c,ws in covers.items() if c not in needed}

        # Nothing left to do? Then update the answer.
        if not covers:
            if len(regex) < len(answer[0]):
                answer[0] = regex
            return

        # Stop when already too bad
        if len(regex)+1+min(len(c) for c in covers) >= len(answer[0]):
            return

        # Try with and without the component looking best
        best = max(covers, key=lambda c: 3 * len(covers[c]) - len(c))
        search(regex + '|' + best, {c:ws-covers[best] for c,ws in covers.items()})
        covers.pop(best)
        search(regex, covers)

    # Setup, search, answer
    answer = ['|'.join('^'+w+'$' for w in winners)]
    search('', {c:matches(c, winners) for c in regex_components(winners, losers)})
    return answer[0][1:]

class Match:
    def __init__(self,
                 search_space=None,
                 start=None,
                 length=None,
                 start_idx=0):

        """ start_idx is the idx where the search space begins in the overall
        search_string.
        start is the start of the match within the particular substring (called
        search_space in this case)
        """
        if search_space:
            self.value = search_space[start: length]
            end = start_idx + start + length - 1
            self.span = (start+start_idx, end)
        else:
            self.value = None
            self.span = None

    def __repr__(self):
        if(self.value):
            return "MatchObj: " + str(self.value) + " " + str(self.span)
        else:
            return "None"

    # def __str__(self):
    #     return self.value or "None"

    def has_value(self):
        if self.value:
            return True
        else:
            return False

    def get_value(self):
        return self.value

    def get_span(self):
        return self.span


def remove_overlaps(match_list):
    # TODO: this is a weird, half-functional, half-imperative implementation
    # that was written at the end of a long day. It WORKS, but needs to be
    # rewritten

    if len(match_list) == 0 or len(match_list) == 1:
        return match_list

    # the following algo relies on the fact that the elems are sorted
    match_list.sort(key=lambda x: x.get_span())

    def helper(rem, elem, accum):
        if len(rem) == 0:
            accum.append(elem)
            return accum
        else:
            accum.append(elem)
            prev_start, prev_end = elem.get_span()
            for x, i in zip(rem, range(len(rem))):
                # if prob, rem =
                start, _ = x.get_span()
                if start > prev_end:
                    return helper(rem[i+1:], x, accum)
            return accum

    elem = match_list[0]
    rem = match_list[1:]
    accum = []
    return helper(rem, elem, accum)


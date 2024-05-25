import argparse

# Create a parser for arguments
parser = argparse.ArgumentParser(description='Hirschberg algorithm')
# add arguments
parser.add_argument('-t', required=False, action='store_true', help='Print every (i,j) on Hirschberg algorithm')
parser.add_argument('-f', required=False, action='store_true', help='Accept files as input')
parser.add_argument('-l', required=False, action='store_true', help='Match whole lines instead of characters')
parser.add_argument('gap', type=int)
parser.add_argument('match', type=int)
parser.add_argument('differ', type=int)
parser.add_argument('aa', type=str)
parser.add_argument('bb', type=str)
args = parser.parse_args()
# Save everything to local variables:
gap, match, differ, aa, bb, t, f, l = args.gap, args.match, args.differ, args.aa, args.bb, args.t, args.f, args.l


def createf(a: [], b: []) -> []:
    """
    Create f array from the two arrays
    :return: table f to find the alignments with EnumerateAlignments()
    """
    ff = [[0 for x in range(2 if len(a) > 1 else len(b) + 1)] for y in range(2 if len(b) > 1 else len(a) + 1)]
    for i in range(len(ff)):  # a
        for j in range(len(ff[i])):  # b
            if i == 0:
                ff[i][j] = gap * j
            elif j == 0:
                ff[i][j] = gap * i
            else:
                ff[i][j] = max(ff[i - 1][j] + gap, ff[i][j - 1] + gap,
                               (ff[i - 1][j - 1] + (match if a[i - 1] == b[j - 1] else differ)))
    return ff


def compare(a: str, b: str) -> int:
    """
    Calculate score between two chars
    :return: (int) score
    """
    if a == b:
        return match
    else:
        return differ


def FinalScore(w1: [], z1: []) -> []:
    """
    Alignment score of the two []
    :return: (int) the final score
    """
    assert len(w1) == len(z1)
    score = 0
    for i in range(len(w1)):
        if w1[i] == '-' or z1[i] == '-':
            score += gap
        elif w1[i] == z1[i]:
            score += match
        else:
            score += differ
    return score


def ComputeAlignmentScore(a: [], b: []) -> []:
    """
    Receives the two arrays to be aligned
    :return: last line of f table
    """
    ll = [j * gap for j in range(len(b) + 1)]
    k = [0] * (len(b) + 1)
    for i in range(1, len(a) + 1):
        ll, k = k, ll
        ll[0] = i * gap
        for j in range(1, len(b) + 1):
            md = compare(a[i - 1], b[j - 1])
            ll[j] = max(ll[j - 1] + gap, k[j] + gap, k[j - 1] + md)
    return ll


def bestalignments(lw: [], lz: []) -> ([], []):
    """
    Accepts the lists of [] with all alignments
    :return: w_max,z_max --> those with the best score
    """

    assert len(lw) == len(lz)
    # Assume first is the best alignment
    w_max = [lw[0]]  # Lists of lists (only with 1 element)
    z_max = [lz[0]]
    score_max = FinalScore(w_max[0], z_max[0])  # Score of first
    for k in range(1, len(lw)):
        score = FinalScore(lw[k], lz[k])  # Score of k alignment
        if score > score_max:
            w_max = [lw[k]]
            z_max = [lz[k]]
        elif score == score_max:
            # Don't add duplicates
            flag = True  # Assume it isn't a duplicate
            for i in range(len(w_max)):
                if w_max[i] == lw[k] and z_max[i] == lz[k]:
                    flag = False  # Means combination is in lists
            if flag:  # flag remained true so add
                w_max.append(lw[k])
                z_max.append(lz[k])

    return w_max, z_max


counter = 0


def hirschberg(a, b):
    """
    Main algorithm accepting the two [] to match
    :return: list with all possible [] combinations of a and b
    """
    global counter
    counter += 1
    w_list = []  # Lists of our main method
    z_list = []

    # This method doesn't return anything but updates w,z list accordingly
    def EnumerateAlignments(a, b, ff, w, z):
        i = len(a)
        j = len(b)
        if i == 0 == j:  # both a,b are empty
            w_list.append([i for i in w])
            z_list.append([i for i in z])
        if i > 0 and j > 0:
            m = compare(a[i - 1], b[j - 1])
            if ff[i][j] == ff[i - 1][j - 1] + m:
                EnumerateAlignments(a[0:i - 1], b[0:j - 1], ff, [a[i - 1]] + w, [b[j - 1]] + z)
        if i > 0 and ff[i][j] == ff[i - 1][j] + gap:
            EnumerateAlignments(a[0:i - 1], b, ff, [a[i - 1]] + w, ['-'] + z)
        if j > 0 and ff[i][j] == ff[i][j - 1] + gap:
            EnumerateAlignments(a, b[0:j - 1], ff, ['-'] + w, [b[j - 1]] + z)

    def NeedlemanWunsch(a, b):
        # Find the best alignments
        ftable = createf(a, b)
        EnumerateAlignments(a, b, ftable, [], [])

    if len(a) == 0:
        w_list.append(list('-' * len(b)))
        z_list.append(b)
    elif len(b) == 0:
        w_list.append(a)
        z_list.append(list('-' * len(a)))
    elif len(a) == 1 or len(b) == 1:
        NeedlemanWunsch(a, b)  # updates w,z lists with all alignments
        w_list, z_list = bestalignments(w_list, z_list)  # Keep only the best
    else:
        # Split a-->(al+ar)
        i = int(len(a) / 2)
        al = a[0:i]
        ar = a[i:]
        sl = ComputeAlignmentScore(al, b)
        sr = ComputeAlignmentScore(ar[::-1], b[::-1])
        s = [sl[i] + sr[-(i + 1)] for i in range(len(b) + 1)]
        maxscore = max(s)  # Find the best score
        j_max = [i for i in range(len(s)) if s[i] == maxscore]  # Breakpoints of b (all with the best score)
        for j in j_max:
            if t:  # Print i,j pairs if it is asked
                print(str(i) + ', ' + str(j))
            # Save split alignments
            wwl, zzl = hirschberg(al, b[0:j])
            wwr, zzr = hirschberg(ar, b[j:])
            # Add each combination to the lists
            for il in range(len(wwl)):
                for ir in range(len(wwr)):
                    w_list.append(wwl[il] + wwr[ir])
                    z_list.append(zzl[il] + zzr[ir])

            # And keep only the best
            w_list, z_list = bestalignments(w_list, z_list)
    return w_list, z_list


if f and l:  # files line to line
    # read file lines into lists
    with open(aa) as f:
        la = [i.strip('\n') for i in f.readlines()]
    with open(bb) as f:
        lb = [i.strip('\n') for i in f.readlines()]

    w, z = hirschberg(la, lb)
    assert len(w) == len(z)
    for k in range(len(w)):
        for i in range(len(w[k])):
            line_a = w[k][i]
            line_b = z[k][i]
            if line_a == line_b:
                print('= ' + ''.join(map(str, line_a)))
                print('= ' + ''.join(map(str, line_b)))
            else:
                print('< ' + ''.join(map(str, line_a)))
                print('> ' + ''.join(map(str, line_b)))
else:
    if f:  # Files but char to char
        with open(aa) as f:
            aa = f.read()
        with open(bb) as f:
            bb = f.read()

    # In all cases now aa,bb are the string to be aligned

    ww, zz = hirschberg([i for i in aa], [i for i in bb])
    assert len(ww) == len(zz)
    for i in range(len(ww)):
        print(''.join(map(str, ww[i])))
        print(''.join(map(str, zz[i])))
        print()

import kgp

HOST = "wss://kalah.kwarc.info/socket"
PORT = 2671
TOKEN = "rengongzhizhang"
AUTHORS = ["1", "2", "3", "4"]
NAME = "This is an example"
ENABLE_DEBUG = True


def evaluate(state):
    return state[kgp.SOUTH] - state[kgp.NORTH]


def abtree(state, depth, side, alpha=-1000, beta=1000):
    result = []
    for move in state.legal_moves(side):
        after, again = state.sow(side, move)
        value = evaluate(after)
        if side == kgp.SOUTH:  # max
            if after.is_final() or depth == 0:
                alpha = value if alpha < value else alpha
                if alpha > beta:
                    return
                else:
                    result.append((value, move))
            else:
                if again:
                    ########################################################
                    child = abtree(after, depth, side, alpha, beta)
                    ########################################################
                else:
                    child = abtree(after, depth - 1, not side, alpha, beta)
                if child:
                    child.sort(key=lambda x: x[0], reverse=False)
                    value = child[0][0]
                    alpha = value if alpha < value else alpha
                    if alpha > beta:
                        return
                    else:
                        result.append((value, move))
        else:
            if after.is_final() or depth == 0:
                beta = value if beta < value else beta
                if alpha > beta:
                    return
                else:
                    result.append((value, move))
            else:
                if again:
                    ########################################################
                    child = abtree(after, depth, side, alpha, beta)
                    ########################################################
                else:
                    child = abtree(after, depth - 1, not side, alpha, beta)
                if child:
                    child.sort(key=lambda x: x[0], reverse=True)
                    value = child[0][0]
                    beta = value if beta < value else beta
                    if alpha > beta:
                        return
                    else:
                        result.append((value, move))
    result.sort(key=lambda x: x[0], reverse=True)
    return result


def ab(state, depth, side, alpha, beta):
    if depth == 0:
        return evaluate(state)
    for move in state.legal_moves(side):
        after, again = state.sow(side, move)
        if after.is_final():
            return evaluate(after)
        if again:
            value = ab(after, depth, side, alpha, beta)
        else:
            value = -ab(after, depth - 1, not side, -beta, -alpha)
        if value >= beta:
            return beta
        if value > alpha:
            alpha = value
    return alpha


def search(state, depth, side):
    # state = Board(0, 0, [4, 4, 4, 4, 4, 4], [4, 4, 4, 4, 4, 4])
    def child(move):
        if depth <= 0:
            return evaluate(state), move

        after, again = state.sow(side, move)
        if after.is_final():
            return evaluate(after), move
        if again:
            return search(after, depth, side)[0], move
        else:
            return search(after, depth - 1, not side)[0], move

    choose = max if side == kgp.SOUTH else min
    return choose((child(move) for move in state.legal_moves(side)), key=lambda ent: ent[0])


def agent(state):
    # state = Board(0, 0, [4, 4, 4, 4, 4, 4], [4, 4, 4, 4, 4, 4])
    # for depth in range(1, 16):
    #    yield search(state, depth, kgp_new.SOUTH)[1]
    size = len(state.south_pits)
    if state.south_pits[size - 1] == 1:
        yield size - 1
    for n in reversed(range(size - 1)):
        if state.south_pits[n] == size - n:
            yield n
    for n in range(size - 1):
        if state.south_pits[n] >= 1:
            yield n


if __name__ == "__main__":
    kgp.connect(agent=agent)
    '''
    kgp_new.connect(agent=agent,
                    host=HOST,
                    port=PORT,
                    token=TOKEN,
                    debug=ENABLE_DEBUG)
    '''
    '''
    kgp.connect(agent=agent,
                host=HOST,
                port=PORT,
                token=TOKEN,
                name=NAME,
                authors=AUTHORS,
                debug=ENABLE_DEBUG)
    '''

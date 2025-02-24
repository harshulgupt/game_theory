import random

def tit_for_tat(history, noise=0):
    if not history or (random.random() < noise):
        return "C"
    return "C" if history[-1] == "C" else "D"

def always_cooperate(history, noise=0):
    return "C"

def always_defect(history, noise=0):
    return "D"

def tit_for_two_tats(history, noise=0):
    if not history or len(history) < 2 or (random.random() < noise):
        return "C"
    return "C" if history[-2:] != ["D", "D"] else "D"

def generous_tit_for_tat(history, noise=0, forgiveness=0.1):
    if not history or (random.random() < noise):
        return "C"
    if history[-1] == "D" and random.random() > forgiveness:
        return "D"
    return "C"

def tester(history, noise=0):
    if not history:
        return "D"
    if len(history) == 1:
        return "C" if history[0] == "D" else "D"
    return tit_for_tat(history, noise)

def random_strategy(history, noise=0):
    return "C" if random.random() > 0.5 else "D"

def grudger(history, noise=0):
    if "D" in history:
        return "D"
    return "C"

def play_game(strategy1, strategy2, rounds=200, randomness=True, noise=0):
    history1, history2 = [], []
    total_rounds = rounds if not randomness else random.randint(rounds - 50, rounds + 50)
    for _ in range(total_rounds):
        move1, move2 = strategy1(history2, noise), strategy2(history1, noise)
        history1.append(move1)
        history2.append(move2)
    return history1, history2

def score(history1, history2):
    score1, score2 = 0, 0
    for m1, m2 in zip(history1, history2):
        if m1 == "C" and m2 == "C":
            score1 += 3
            score2 += 3
        elif m1 == "C" and m2 == "D":
            score2 += 5
        elif m1 == "D" and m2 == "C":
            score1 += 5
        else:
            score1 += 1
            score2 += 1
    return score1, score2

def tournament(strategies, rounds=200, noise=0):
    results = {s.__name__: 0 for s in strategies}
    for i, strat1 in enumerate(strategies):
        for j, strat2 in enumerate(strategies):
            if i < j:
                h1, h2 = play_game(strat1, strat2, rounds, noise=noise)
                s1, s2 = score(h1, h2)
                results[strat1.__name__] += s1
                results[strat2.__name__] += s2
    return sorted(results.items(), key=lambda x: x[1], reverse=True)

strategies = [tit_for_tat, always_cooperate, always_defect, tit_for_two_tats, generous_tit_for_tat, tester, random_strategy, grudger]
noise_level = 0.05
results = tournament(strategies, noise=noise_level)
for strategy, points in results:
    print(f"{strategy}: {points}")

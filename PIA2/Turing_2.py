#!/usr/bin/env python3
from functools import reduce
from typing import Dict, Set, Tuple


def or_function(v1: bool, v2: bool) -> bool:
    return v1 or v2


def turing_machine(sigma: Set[chr],
                   gamma: Set[chr],
                   b: chr,
                   delta: Dict[Tuple[str, chr], Tuple[str, chr, int]],
                   f: Set[str],
                   s: str,
                   max_iter: int = 10000):

    def delta_fn(state: str, char: chr) -> Tuple[str, str, int]:
        print(f'{state}, {char} : {delta.get((state, char), "_")}')
        return delta.get((state, char), ("q_i", char, 0))

    def evaluate_word(word: str):
        return evaluate(b+word+b, 1, s, 1)

    def evaluate(word: str,
                 head_position: int,
                 state: chr,
                 iter_num: int) -> str:
        if word[0] != b or head_position < 0:
            evaluate(b + word, head_position + 1, state, iter_num)
        if word[-1] != b or head_position >= len(word):
            evaluate(word + b, head_position, state, iter_num)
        print(f'w: {word[:head_position]}|{word[head_position]}|{word[head_position+1:]}')
        (new_state, new_char, direction) = delta_fn(state, word[head_position])
        if new_state == "q_i" or iter_num > max_iter:
            return "Rejected"
        if new_state in f and direction == 0:
            return "Accepted"
        return evaluate(word[:head_position] + new_char + word[head_position+1:],
                        head_position + direction,
                        new_state,
                        iter_num + 1)

    if reduce(or_function, (v not in gamma for k, v in delta.keys())):
        raise Exception(f'char in delta is not in gamma {[v for k, v in delta.keys()]}')
    return evaluate_word


if __name__ == "__main__":
    # Transiciones para wcw^-1|w ϵ a,b}*}
    delta = {
        ('q_0', 'a'): ('q_1', 'A', 1),
        ('q_0', 'b'): ('q_1', 'B', 1),
        ('q_0', '@'): ('q_f', '@', 0),
        ('q_1', 'a'): ('q_1', 'a', 1),
        ('q_1', 'b'): ('q_1', 'b', 1),
        ('q_1', '@'): ('q_2', '@', -1),
        ('q_2', 'a'): ('q_2', 'a', -1),
        ('q_2', 'b'): ('q_2', 'b', -1),
        ('q_2', '@'): ('q_3', '@', 1),  # Nueva transición
        ('q_3', 'a'): ('q_3', 'a', 1),
        ('q_3', 'b'): ('q_3', 'b', 1),
        ('q_3', '@'): ('q_f', '@', 0),
    }

    # Configuración inicial para wcw^-1|w ϵ a,b}*}
    stri = 'abbabba'
    sigma = {'a', 'b'}
    b = '@'  # Símbolo en blanco
    gamma = {b, 'a', 'b'} | sigma
    f = {'q_f'}
    s = 'q_0'

    tm = turing_machine(sigma, gamma, b, delta, f, s)
    print(tm(stri))

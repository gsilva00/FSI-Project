# CTF 7 - Week 10 - Classical Cipher

## Introduction

In this CTF challenge, we were given an excerpt of a Portuguese newspaper that is encrypted with a classical cipher. The excerpt is the following:

```plaintext
-!$_):!*.;^;,):*%(;%*)&),#$)%,;(;)$~[%()>)&!%,)+!,:)*))~;(&!,),:;-[!,:*)[%-!,&!_!@!;(#$;!,-!+[%+;+[)%,:!&;*)!-!+[)*$():!&*!,),;@$+&)~%+>)>))*;@%,[)*#$;+!,-!+|*!+[!,;+[*;)(<),),|!*()-!;,).)+[)@;(:;+&;:)*)!,.%,%[)+[;,#$;@)+>)*)(:;*&;*)(;;(:)[)*)(-%+-!);#$%:):!*[$@$;,)&;[;+%,;,[)).;+-;*-!(!,;:*;.%))%*~)+&):!*)!|%(&!:*%(;%*!&%)&):)*[%&))-!+[)*:)*))*!+&)%+)$@$*)~&)[)-)&).%,#$;>!_;:*!,,;@$;+),%+,[)~)-!;,&!-~$<;&;[;+%,&!:!*[!>!_;;!&%)):*)^)&!:)*))#$;&)&)|:|(),,;!$[*),)%&)+)!&;,-!<*%*)[;~)!@*$:!~%&;*)&!{>$,!*>;@|*#!&;;:}
```

### Frequency Analysis (Ciphered Portuguese Text)

The first step to decrypt the text is to perform a frequency analysis of the characters in the text. This analysis will help us to identify the most common characters in the text, which will help when comparing with the Portuguese language.

Therefore, we're going to reuse the [script](/files/CTF10/freq.py) provided for [LOGBOOK9](LOGBOOK9.md) with `python3 freq.py`:

```plaintext
-------------------------------------
1-gram (top 20):
): 87 (16.80%)
;: 54 (10.42%)
!: 52 (10.04%)
*: 41 (7.92%)
,: 38 (7.34%)
%: 30 (5.79%)
&: 30 (5.79%)
+: 26 (5.02%)
:: 25 (4.83%)
[: 24 (4.63%)
$: 20 (3.86%)
(: 17 (3.28%)
-: 16 (3.09%)
@: 10 (1.93%)
~: 9 (1.74%)
#: 8 (1.54%)
>: 8 (1.54%)
.: 6 (1.16%)
|: 6 (1.16%)
_: 4 (0.77%)
-------------------------------------
2-gram (top 20):
*): 16 (3.09%)
)*: 12 (2.32%)
-!: 11 (2.13%)
&): 11 (2.13%)
!,: 11 (2.13%)
[): 10 (1.93%)
,): 8 (1.55%)
)&: 8 (1.55%)
),: 8 (1.55%)
%,: 8 (1.55%)
&!: 8 (1.55%)
)): 8 (1.55%)
+[: 8 (1.55%)
;+: 8 (1.55%)
&;: 8 (1.55%)
):: 7 (1.35%)
:!: 7 (1.35%)
;,: 7 (1.35%)
#$: 7 (1.35%)
,;: 7 (1.35%)
-------------------------------------
3-gram (top 20):
)*): 6 (1.16%)
:)*: 5 (0.97%)
#$;: 5 (0.97%)
):!: 4 (0.78%)
:!*: 4 (0.78%)
)&): 4 (0.78%)
-!+: 4 (0.78%)
!+[: 4 (0.78%)
+[): 4 (0.78%)
[)*: 4 (0.78%)
;,): 3 (0.58%)
,#$: 3 (0.58%)
)&!: 3 (0.58%)
*)): 3 (0.58%)
,),: 3 (0.58%)
,&!: 3 (0.58%)
,-!: 3 (0.58%)
!&;: 3 (0.58%)
&;*: 3 (0.58%)
;*): 3 (0.58%)
```

According to the guidelines, the flag is between `{}`, which are characters that aren't ciphered, at the end of each cipher. Therefore, the main goal is to decode the characters `>$,!*>;@|*#!&;;:`.

Given that words of portuguese origin don't use the letters `K`, `W`, `Y`, but nowadays there are "borrowed" words that are used with them, we can't exclude the possibility. We can, however, guarantee that they will be extremely rare (last places) in the frequency analysis tables.

This assumption is proven by the frequency analysis of the Portuguese language, which is the following:

### Frequency Analysis (Plaintext Portuguese Text)

#### Single Letters

| Letter | Frequency (Source 1) | Frequency (Source 2) |
| ------ | -------------------- | -------------------- |
| a      | 14.63%               | 13.9%                |
| e      | 12.57%               | 12.2%                |
| o      | 10.73%               | 10.8%                |
| s      | 7.81%                | 7.9%                 |
| r      | 6.53%                | 6.9%                 |
| i      | 6.18%                | 6.9%                 |
| n      | 5.05%                | 5.3%                 |
| d      | 4.99%                | 5.4%                 |
| m      | 4.74%                | 4.2%                 |
| u      | 4.63%                | 4.0%                 |
| t      | 4.34%                | 4.9%                 |
| c      | 3.88%                | 4.4%                 |
| l      | 2.78%                | 2.8%                 |
| p      | 2.52%                | 2.9%                 |
| v      | 1.67%                | 1.3%                 |
| g      | 1.30%                | 1.2%                 |
| h      | 1.28%                | 0.8%                 |
| q      | 1.20%                | 0.9%                 |
| b      | 1.04%                | 1.0%                 |
| f      | 1.02%                | 1.0%                 |
| z      | 0.47%                | 0.4%                 |
| j      | 0.40%                | 0.4%                 |
| x      | 0.21%                | 0.3%                 |
| k      | 0.02%                | 0.1%                 |
| w      | 0.01%                | 0.0%                 |
| y      | 0.01%                | 0.0%                 |

[Source 1](https://pt.wikipedia.org/wiki/Frequ%C3%AAncia_de_letras)
[Source 2](https://www.dcc.fc.up.pt/~rvr/naulas/tabelasPT/)

> Given that the first source didn't have bigram and trigram frequencies, we used a different source for those (as shown below). Therefore, we also included the single letter frequencies from the second source (mostly the same order).

#### Bigrams

| Bigrams | Frequency |
| ------- | --------- |
| es      | 2.071%    |
| de      | 2.033%    |
| os      | 1.826%    |
| ra      | 1.743%    |
| as      | 1.641%    |
| en      | 1.494%    |
| ar      | 1.489%    |
| ad      | 1.480%    |
| do      | 1.445%    |
| re      | 1.416%    |
| co      | 1.400%    |
| se      | 1.347%    |
| er      | 1.333%    |
| nt      | 1.327%    |
| te      | 1.272%    |
| ca      | 1.257%    |
| da      | 1.192%    |
| or      | 1.185%    |
| ao      | 1.184%    |
| an      | 1.162%    |
| ta      | 1.146%    |
| ma      | 1.135%    |
| em      | 1.092%    |
| on      | 1.014%    |
| ac      | 1.005%    |
| st      | 0.980%    |
| od      | 0.958%    |
| qu      | 0.938%    |
| to      | 0.933%    |
| sa      | 0.919%    |
| al      | 0.903%    |

> Originally in frequency out of 1000 characters, we converted to percentage for easier comparison with the frequency analysis of the ciphered text.

[Source](https://www.dcc.fc.up.pt/~rvr/naulas/tabelasPT/)

#### Trigram

| Trigram | Frequency |
| ------- | --------- |
| que     | 0.7229%   |
| ent     | 0.7023%   |
| nte     | 0.5508%   |
| ado     | 0.5116%   |
| ade     | 0.5004%   |
| ode     | 0.4543%   |
| ara     | 0.4537%   |
| est     | 0.4390%   |
| res     | 0.4308%   |
| con     | 0.4173%   |
| com     | 0.4095%   |
| sta     | 0.3095%   |
| dos     | 0.3808%   |
| cao     | 0.3797%   |
| par     | 0.3629%   |
| aca     | 0.3555%   |
| men     | 0.3465%   |
| sde     | 0.3345%   |
| ica     | 0.3305%   |
| ese     | 0.3187%   |
| aco     | 0.3154%   |
| ada     | 0.3145%   |
| por     | 0.3139%   |
| nto     | 0.3114%   |
| ose     | 0.3082%   |
| des     | 0.3051%   |
| ase     | 0.2776%   |
| era     | 0.2718%   |
| oes     | 0.2660%   |
| uma     | 0.2573%   |
| tra     | 0.2566%   |
| ida     | 0.2555%   |
| dad     | 0.2484%   |
| ant     | 0.2454%   |
| are     | 0.2430%   |
| ont     | 0.2405%   |
| pre     | 0.2404%   |
| ist     | 0.2391%   |
| ter     | 0.2389%   |
| ais     | 0.2337%   |

> Originally in frequency out of 10000 characters, we converted to percentage for easier comparison with the frequency analysis of the ciphered text.

[Source](https://www.dcc.fc.up.pt/~rvr/naulas/tabelasPT/)

## Decryption

There a lot of uncertainties in this challenge, compared to [LOGBOOK9](/LOGBOOK9.md), given the small size of the text and the lack of spaces in the ciphertext. So we will probably have to make many assumptions, less founded, and backtrack more often.

Given that the most common characters used in Portuguese plaintext are vowels, our first approach will be to focus on them, as the ciphered text is likely to have a lot of vowels as well, and they make the ciphertext easier to read and decrypt (even without spaces in between words).

The reliability of the ciphertext frequency analysis of bigrams and trigrams is very low, for two reasons:

- the text is very small, making the frequency of the characters sometimes inconsistent with the frequency analysis of the Portuguese language;
- the ciphertext has no spaces, which leads to a lot of bigrams and trigrams that are not actually part of the same word - the opposite of how they are identified in the frequency analysis. Naturally, this worsens as the bigrams and trigrams become less common.

Even so, we will still cautiously use them, as the vowels we decipher are part of many bigrams and trigrams that are common in Portuguese, and it might help find another.

### Try 1

Given the large gap in frequency between the 1st and 2nd common characters in the Portuguese language being matched by ciphered text, we can assume that the most common character in the ciphered text is the letter `a`.

So, we executed the following command to decipher the first letter of the ciphertext:

```bash
tr ')' 'a' < L12G02.cph > files/CTF10/plaintext_try1.txt
```

Due to the lack of spaces in the ciphertext, it is hard to tell if this decryption is correct by the letter positioning like we did in [LOGBOOK9](/LOGBOOK9.md). But we will continue to decrypt the rest and see if it makes sense, backtracking if necessary.

Letters deciphered so far:

| Ciphertext | Plaintext |
| ---------- | --------- |
| )          | a         |

Flag progression (0%): `{>$,!*>;@|*#!&;;:}`

The result can be seen [here](/files/CTF10/plaintext_try1.txt).

### Try 2

Looking at the trigrams, and assuming that the previous step is correct, `)*)` should be `ara` - which is a relatively common trigram in Portuguese. This matches the most common ciphertext bigrams `*)` and `)*` with the `ra` and `ar` being common bigrams in Portuguese.

Therefore, we can assume that `*` is `r`.

```bash
tr ')*' 'ar' < L12G02.cph > files/CTF10/plaintext_try2.txt
```

`aca` and `ada` are also possibilities for the trigram, although the corresponding bigrams are not as common in Portuguese. On the same note, the 6th most common trigram `)&)` can be one of those as well, but we will not use it for now.

We will continue to decrypt the text, so that we can have a better understanding of the text and evaluate if the previous steps were correct.

Letters deciphered so far:

| Ciphertext | Plaintext |
| ---------- | --------- |
| )          | a         |
| \*         | r         |

Flag progression (12.5%): `{>$,!r>;@|r#!&;;:}`

The result can be seen [here](/files/CTF10/plaintext_try2.txt).

### Try 3

Trying to shift our focus to the other vowels, we can see that `;` and `!` are the next most common characters in the ciphertext. So, despite the extremely close in frequency, 52 and 54, respectively, we will assume that the 2nd most common character in the ciphertext is `e` (`;`) and the 3rd most common character is `o` (`!`).

```bash
tr ')*;!' 'areo' < L12G02.cph > files/CTF10/plaintext_try3.txt
```

Letters deciphered so far:

| Ciphertext | Plaintext |
| ---------- | --------- |
| )          | a         |
| \*         | r         |
| ;          | e         |
| !          | o         |

Flag progression (43.75%): `{>$,or>e@|r#o&ee:}`

The result can be seen [here](/files/CTF10/plaintext_try3.txt).

### Try 4

Given that `&` is a common character in the ciphertext, and it precedes the letters we assume are the vowels `a`, `e` and `o`, as well as succeeding `a` as well, we can try and assume that `&` is `d` (curiously the single letter frequency of `d` is very close to the frequency of `&`).

```bash
tr ')*;!&' 'areod' < L12G02.cph > files/CTF10/plaintext_try4.txt
```

Letters deciphered so far:

| Ciphertext | Plaintext |
| ---------- | --------- |
| )          | a         |
| \*         | r         |
| ;          | e         |
| !          | o         |
| &          | d         |

Flag progression (50%): `{>$,or>e@|r#odee:}`

The result can be seen [here](/files/CTF10/plaintext_try4.txt).

### Try 5

There are several places in the [previous decryption](/files/CTF10/plaintext_try4.txt) where `:` looks like it can be a `p` (`:ara`, `:oderao`, `:erdera`, ``), but it is impossible to be sure, due to the lack of spaces. We will assume it either way, and see if it makes sense.

```bash
tr ')*;!&:' 'areodp' < L12G02.cph > files/CTF10/plaintext_try5.txt
```

A couple of words can now be recognized in the text, if we separate them from the surrounding characters in order to have something recognizable there (wishful, obviously). This, therefore, still makes us completely unsure of the correctness of the decryption.

Letters deciphered so far:

| Ciphertext | Plaintext |
| ---------- | --------- |
| )          | a         |
| \*         | r         |
| ;          | e         |
| !          | o         |
| &          | d         |
| :          | p         |

Flag progression (56.25%): `{>$,or>e@|r#odeep}`

The result can be seen [here](/files/CTF10/plaintext_try5.txt).

### Try 6

Going back to the most reliable part of the frequency analysis, the single letter frequency, we'll focus on making educated guesses on the next common characters (`,` and `%`), which, in terms of frequency, are around the already deciphered letters in the ciphertext.

In the same line of thinking, by frequency alone, `s`, `i`, `n` could be good guesses, because these are the options around the already deciphered letters in the frequency analysis of the Portuguese language.

The bigrams containing `,` - some more common, others less common, either contain the deciphered vowels or `&` - (`!,`, `,)`, `),`, `;,`, `,;` and `%,`). By comparing with the plaintext bigrams, we can with some confidence say that `,` is `s`.

```bash
tr ')*;!&:,' 'areodps' < L12G02.cph > files/CTF10/plaintext_try6.txt
```

Letters deciphered so far:

| Ciphertext | Plaintext |
| ---------- | --------- |
| )          | a         |
| \*         | r         |
| ;          | e         |
| !          | o         |
| &          | d         |
| :          | p         |
| ,          | s         |

Flag progression (62.5%): `{>$sor>e@|r#odeep}`

The result can be seen [here](/files/CTF10/plaintext_try6.txt).

### Try 7

Even after this transformation, the text is still very hard to read. So we had an alternative idea: to try and find long words in the text.

Because the ciphertext has no spaces, every combination of letters can effectively be a long "word" in the text. The higher the `N_GRAM` value, the bigger the amount of 1-frequency "words" we'll find. The goal is to find the combinations that have the highest frequency, which means that they show up together more often in the text, and are more likely to be actual words.

Not only did we increase the N_GRAM value, but we also used the text from the previous decryption, to make finding the words easier:

```python
# From:
N_GRAM = 3
# To:
N_GRAM = 20
# ...
# From:
with open('L12G02.cph') as f:

# To:
with open('plaintext_try6.txt') as f:
```

Due to the length of the output, it can be found [here](/files/CTF10/20ngram_output.txt).

Even though, the top 20 of the 7-grams is the highest amount of characters in which the 1st entry is not a 1-frequency group of characters, the 2 entries with frequency 2 do not provide us much information. The same applies to the other top 20 n-grams.

So we fell back to looking at the frequency analysis of single letters and guessing, and we can see that the vowel `i` is the next most common character in the Portuguese language, and has a similar enough frequency to `%` in the ciphertext. So we will assume that `%` is `i`, and we'll keep `n` as a possibility for when we have to backtrack.

```bash
tr ')*;!&:,%' 'areodpsi' < L12G02.cph > files/CTF10/plaintext_try7.txt
```

Letters deciphered so far:

| Ciphertext | Plaintext |
| ---------- | --------- |
| )          | a         |
| \*         | r         |
| ;          | e         |
| !          | o         |
| &          | d         |
| :          | p         |
| ,          | s         |
| %          | i         |

Flag progression (62.5%): `{>$sor>e@|r#odeep}`

The result can be seen [here](/files/CTF10/plaintext_try7.txt).

### Try 8

After this substituition, some words containing `i` and `s` can be recognized and the 2-frequency 7-gram `pr%(e%r` became `pri(eira` and `pri(eiro`, which are very likely to be `primeira` and `primeiro`, respectively. This lead us to believe `(` is `m`.

```bash
tr ')*;!&:,%(' 'areodpsim' < L12G02.cph > files/CTF10/plaintext_try8.txt
```

Letters deciphered so far:

| Ciphertext | Plaintext |
| ---------- | --------- |
| )          | a         |
| \*         | r         |
| ;          | e         |
| !          | o         |
| &          | d         |
| :          | p         |
| ,          | s         |
| %          | i         |
| (          | m         |

Flag progression (62.5%): `{>$sor>e@|r#odeep}`

The result can be seen [here](/files/CTF10/plaintext_try8.txt).

### Try 9

After the last substitution, more words are recognizable, so we decided to separate the words we were able to recognize with spaces (for example, assuming that every `paraa` is `para a`) and we got the following:

```plaintext
-o$_apor.e^es a primeira das #$aisemea$~[ima>a dois a+os para a~em dos aspe-[ospra[i-osdo_o@oem#$eos-o+[i+e+[ais poderao -o+[ar$mapodrosase@$+da~i+>a>aare@is[ar#$e+os-o+|ro+[ose+[ream<asas|orma-oesa.a+[a@empe+deparaos.isi[a+[es#$e@a+>aram perderam e empa[aram -i+-oae#$ipapor[$@$esade[e+ises[aa.e+-er-omosepre.iaair~a+daporao|im do primeiro dia da par[ida a-o+[ar para a ro+dai+a$@$ra~da[a-ada.is#$e>o_eprosse@$e+asi+s[a~a-oesdo-~$<ede[e+isdopor[o>o_eeo dia a pra^ado para a #$edada|p| mas seo$[rasaida+aodes-o<rira[e~ao@r$po~iderado{>$sor>e@|r#odeep}
```

With the habitual low degree of certainty, we can recognize parts such as `aspe-[ospra[i-os`, `empa[aram`, `primeiro dia da part[ida`, that we are going to decipher as `-` being `c` (as both `aspectos` - even in the old orthographic agreement is recognizable - and `praticos` share letters in very obvious stops) and `[` being `t` and observe if the text makes sense.

```bash
tr ')*;!&:,%(-[' 'areodpsimct' < L12G02.cph > files/CTF10/plaintext_try9.txt
```

> For some reason, substituting `[` for `t` completely broke the text, inserting a huge amount of `t`s in the text, so we'll use the find and replace function in VSCode, for this and future substitutions.

Then, as before, we separate more words

```plaintext
co$_apor.e^es a primeira das #$aisemea$~tima>a dois a+os para a~em dos aspectos praticos do _o@oem#$eosco+ti+e+tais poderao co+tar$ma podrosase@$+da~i+>a>aare@istar#$e+osco+|ro+tose+tream<asas|ormacoesa.a+ta@empe+de para os .isita+tes#$e@a+>aram perderam e empataram ci+co a e#$ipa port$@$esa de te+is esta a.e+cercomosepre.iaair~a+daporao|imdoprimeirodiadapartidaaco+tar para a ro+dai+a$@$ra~datacada.is#$e>o_eprosse@$e+asi+sta~acoesdoc~$<edete+is do porto>o_eeodiaapra^ado para a#$edada|p|mas se o$tra saida+aodesco<rirate~ao@r$po~iderado{>$sor>e@|r#odeep}
```

Letters deciphered so far:

| Ciphertext | Plaintext |
| ---------- | --------- |
| )          | a         |
| \*         | r         |
| ;          | e         |
| !          | o         |
| &          | d         |
| :          | p         |
| ,          | s         |
| %          | i         |
| (          | m         |
| -          | c         |
| [          | t         |

Flag progression (62.5%): `{>$sor>e@|r#odeep}`

The result can be seen [here](/files/CTF10/plaintext_try9.txt).

### Final Result

Following the same of process of making increasingly more educated guesses, as separating words that we can recognize becomes easier and highlights other words that we weren't sure about (like `a#$edada|p|masseo$trasaida` becomes `a#$edada|p|mas se o$tra saida`, highlighting `o$tra`, which we can assume is `outra`), we were able to decipher the whole text (through find and replace in VSCode, due to further issues with the first argument of the `tr` command).

Letters deciphered so far:

| Ciphertext | Plaintext |
| ---------- | --------- |
| )          | a         |
| \*         | r         |
| ;          | e         |
| !          | o         |
| &          | d         |
| :          | p         |
| ,          | s         |
| %          | i         |
| (          | m         |
| -          | c         |
| [          | t         |
| $          | u         |
| #          | q         |
| +          | n         |
| ~          | l         |
| <          | b         |
| @          | g         |
| .          | v         |
| \|         | f         |
| >          | h         |
| ^          | z         |
| \_         | j         |

> The letters `k`, `w` and `y` were not present in the ciphertext, as we hypothesized at the start, so we didn't have to guess them. `x` wasn't either.

Flag progression (100%): `{husorhegfrqodeep}`

The final result can be seen [here](/files/CTF10/plaintext_final.txt).

And the final plaintext, with spaces for readability, is the following:

```plaintext
cou ja por vezes a primeira das quais e me a ultima ha dois anos para alem dos aspectos praticos do jogo em que os continentais poderao contar uma podrosa segunda linha ha a registar que nos confrontos entre ambas as formacoes a vantagem pende para os visitantes que ganharam perderam e empataram cinco a equipa portuguesa de tenis esta a vencer como se previa a irlanda por ao fim do primeiro dia da partida a contar para a ronda inaugural da taca davis que hoje prossegue nas instalacoes do clube de tenis do porto hoje e o dia aprazado para a que dada fpf mas se outra saida nao descobrir ate la o grupo liderado {husorhegfrqodeep}
```

> Some aspects of the text lead us to backtrack a couple of times, such as the acronym `fpf`, the weird `cou` start, and the word `podrosa`, which we assume is a typo for `poderosa`.

The flag is, therefore very clearly highlighted with the braces `{husorhegfrqodeep}`. We submitted it in the platform and completed the challenge!

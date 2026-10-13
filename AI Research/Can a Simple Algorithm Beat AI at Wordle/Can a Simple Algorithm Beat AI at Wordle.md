# Can AI Beat Wordle?

## Research topic and question

- How many guesses does AI usually need to solve Wordle? Try it against a simple word-filtering algorithm using the same word list and answers. Who wins more often, and who needs fewer guesses?
- Can you just play the games yourself here, with a program giving you the clues? I want to see how you do against the simple algorithm.

## Research findings

**I averaged 3.87 guesses; the simple algorithm averaged 3.80. Both solved all 30 games.**

| Result | Me (GPT-6-astra) | Filtering algorithm |
|---|---:|---:|
| Solved within six guesses | 30/30 | 30/30 |
| Average guesses | 3.87 | **3.80** |
| Median guesses | 4 | 4 |
| Finished in fewer guesses | 6 games | **9 games** |

The other **15 games were ties**. The algorithm used just two fewer guesses across the entire experiment—a small edge, not convincing evidence of general superiority.

Both used the same [2,315-word dictionary](https://gist.github.com/cfreshman/a03ef2cba789d8cf00c08f767e0fad7b), randomly selected answers, and **SLATE** opener. I chose guesses from the clues without seeing hidden answers or program-filtered candidates. The algorithm eliminated incompatible words and favored common letters.

So, **about four guesses for me in this pilot**. These games shared one conversation; they don’t establish how AI generally performs.
## Import provenance

This introduction was imported from [the GitHub case description](https://github.com/aipoch/open-science-usecases/blob/a27492292020e43cbb0c52a2be5a0fdc4fd9fd7c/Can%20a%20Simple%20Algorithm%20Beat%20AI%20at%20Wordle/Can%20a%20Simple%20Algorithm%20Beat%20AI%20at%20Wordle.md). The archived export and poster retain their original contents. This reorganization did not rerun the study or independently reverify its external sources or conclusions.

## Case files

- [Session export](./Can%20a%20Simple%20Algorithm%20Beat%20AI%20at%20Wordle.science)
- [Case poster](./Can%20a%20Simple%20Algorithm%20Beat%20AI%20at%20Wordle.png)

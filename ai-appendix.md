# ECON 5200 PS2 - AI Transcript

**Model and date:** GPT-6, October 27, 2026

## Version 1 prompt

I'm working on Phase 4 of my ECON 5200 assignment. I need to design a sequential experiment using Python. Can you help me create a simple design with four planned checks and explain how to reduce false positives from repeated testing? Please keep the code and explanation simple.

## Version 1 reply

For Phase 4, you can use a simple sequential experiment with four planned checks. Instead of waiting until the end, we check the results at different sample sizes and stop early if the experiment shows a significant positive effect.

### 1. Python Code

```python
rng = np.random.default_rng(12)

treatment = rng.normal(0.15, 1.0, 1000)
control = rng.normal(0, 1.0, 1000)

looks = [250, 500, 750, 1000]
cutoff = 0.01

for n in looks:
    effect = treatment[:n].mean() - control[:n].mean()
    se = np.sqrt(2 / n)
    p = 2 * stats.norm.sf(abs(effect / se))

    print(n, round(effect, 3), round(p, 4))

    if p < cutoff and effect > 0:
        print("Ship at n =", n)
        break
else:
    print("Do not ship")
```

This code uses NumPy and SciPy, which are already imported in your notebook.

### 2. How It Works

The experiment has four planned checks, at 250, 500, 750, and 1,000 observations per group.

At each check, we calculate the estimated effect and its p-value. If the p-value is below 0.01 and the estimated effect is positive, we stop and ship the experiment. Otherwise, we continue to the next check.

### 3. Why This Reduces False Positives

If we repeatedly check an experiment using `p < 0.05`, the chance of finding a significant result by luck increases.

To address this, we use a stricter cutoff of **0.01 at each of the four checks**.

With four planned tests, the probability of at least one false positive is at most 4% under the null hypothesis, assuming each individual p-value is valid. This keeps the overall false-positive probability below 5%.

This approach works for four predetermined checks, but it should not be used for unlimited checking.

### 4. Short Explanation for the Assignment

I used four planned checks at sample sizes of 250, 500, 750, and 1,000 per group. I set the p-value cutoff to 0.01 to reduce false positives from repeated testing. If the effect is positive and significant, the experiment stops early. Otherwise, it continues to the next check. This makes the decision process more controlled than checking the results whenever we want.

The main advantage is that we can stop successful experiments early while controlling the risk of false positives.

---

## Version 2 prompt

I ran the code and got p-values of 0.3002, 0.0251, and 0.0026 at sample sizes of 250, 500, and 750. The experiment stopped at 750. Can you check if my sequential design controls false positives correctly and improve the explanation? Please keep it simple and explain any changes.

## Version 2 reply

Yes, your sequential design controls false positives correctly under the simulation assumptions. The code is also working as expected.

### 1. Checking the results

| Sample size per group | P-value | Decision |
|---|---|---|
| 250 | 0.3002 | Continue |
| 500 | 0.0251 | Continue |
| 750 | 0.0026 | Ship |

The experiment stops at 750 because the p-value is below 0.01 and the estimated effect is positive.

### 2. Does it control false positives?

Yes. You have four planned checks, each using a cutoff of 0.01.

Using the Bonferroni principle:

4 × 0.01 = 0.04

This means the overall false-positive probability is at most 4% under the null hypothesis, assuming the individual p-values are valid.

Since 4% is below 5%, the design provides conservative control of false positives, even though the repeated checks are not independent.

### 3. Small improvement to the code

You can keep your original code. I would just add this line after defining `cutoff`:

```python
print("False-positive bound:", len(looks) * cutoff)
```

This prints `0.04` and makes the reason for using the stricter cutoff easier to understand.

### 4. Improved explanation for the assignment

I used four planned checks with a p-value cutoff of 0.01. The experiment did not pass at 250 or 500, but it passed at 750 with a p-value of 0.0026.

With four checks, the overall false-positive rate is at most 4% under the null, assuming valid p-values. This is below 5%, so the stricter cutoff helps control false positives from repeated testing.

### 5. What I changed

I kept the same experimental design and stopping rule. I added an explanation of the 4% false-positive bound and connected it to the Bonferroni principle. I also suggested printing that bound in the code. The stopping result remains unchanged.

The main limitation is that this guarantee applies to the four planned checks, not to checking the experiment whenever we want.

---

## Changes made

After Version 1, I ran the simulation and asked AI to check whether the false-positive control was correct.

After Version 2, I kept the same stopping rule and revised the explanation to include the 4% Bonferroni bound.

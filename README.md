# Importance of Moment for Ball-Strike Counts in Baseball Plate Appearances

This repository contains the code and data for the paper **"A measure of the importance of moment for ball-strike counts in a baseball plate appearance"** by Dohyun Lee, Jeongeon Lee, Tonghoon Suk, and Min Kyu Sim. The study constructs a discrete-time Markov Chain (DTMC) model for baseball plate appearances (PA) and introduces the Importance of Moment (IOM) to quantify the criticality of each ball-strike count situation.

## Table of Contents

- [Overview](#overview)
- [Data](#data)
- [Methodology](#methodology)
- [Importance of Moment (IOM)](#importance-of-moment-iom)
- [Results](#results)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Overview

This project provides a comprehensive analysis of how ball-strike counts influence the success of a plate appearance in baseball. It introduces the concept of the Importance of Moment (IOM) and evaluates how different counts can affect the outcomes for the batter and pitcher.

## Data

The dataset includes statistics from Major League Baseball (MLB) games, provided by MLB’s Statcast, covering various aspects of plate appearances, such as:

- Ball-strike counts
- Pitch types and speeds
- Outcomes like hits, walks, and strikeouts

## Methodology

The analysis involves:
1. **Constructing a DTMC Model**: Developing a discrete-time Markov Chain model based on MLB pitch-by-pitch data.
2. **Quantifying IOM**: Introducing the Importance of Moment (IOM) to assess the criticality of different ball-strike counts.
3. **Empirical Validation**: Investigating how IOM explains variations in pitchers’ behavior, particularly fastball speed.

## Importance of Moment (IOM)

The Importance of Moment (IOM) is a novel metric introduced to quantify the criticality of each ball-strike count situation in a baseball PA. It is based on the probabilistic difference between the pitcher’s and hitter’s favorable outcomes (out vs. reaching base). Key aspects include:

- **Critical Counts**: Counts where the probabilistic outcomes for pitcher and hitter vary significantly, indicating a high IOM value.
- **Pitcher’s and Batter’s Advantage**: Evaluating counts that favor either the pitcher or the batter.
- **Empirical Validation**: Correlating higher IOM values with observable behaviors, such as increased fastball speeds by pitchers.

## Results

Key findings from the study include:
- Pitchers tend to throw faster fastballs at counts with higher IOM values.
- Ace pitchers (those who received Cy Young Award votes) tend to pitch even faster in high IOM two-strike situations.
- The DTMC model effectively explains the probabilistic structure of a baseball PA and player behavior.

## Usage

To use the code in this repository, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/importance-of-moment-for-ball-strike-counts.git
    ```
2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Run the analysis:
    ```bash
    python analysis.py
    ```

## Contributing

We welcome contributions to this project. Please submit pull requests or open issues for any bugs or enhancements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## References

For more details, please refer to the full paper on [Taylor & Francis Online](https://doi.org/10.1080/02640414.2024.2355423).

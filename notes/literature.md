# Regime-switching asset allocation: verified literature map

Compiled 2026-10-08. Scope: stocks/bonds/cash allocation under regime switching, with a POMDP / decision-theoretic angle.

## How entries were verified

- **[CR]**: metadata (title, authors, venue, volume(issue):pages, DOI) pulled from the Crossref DOI registry (api.crossref.org) on 2026-10-08.
- **[AX]**: metadata pulled from the arXiv API (export.arxiv.org).
- **[WEB]**: confirmed on a publisher page, Project Euclid, Risk.net, IDEAS/RePEc, Philadelphia Fed, or an author/institutional repository (URL given).
- **[READ]**: I read the paper text (arXiv HTML or the published PDF) for the design details reported here. Entries without [READ] have design notes taken from abstracts or abstract-level summaries only.
- **UNVERIFIED**: anything I could not confirm. Do not cite these without checking.

Year convention: the year of the journal volume/issue. Where Crossref's "issued" date is the earlier online-first year, that is noted.

BibTeX for every verified entry is in `refs.bib` (same folder). Keys are given in brackets after each entry.

---

## 1. Regime models for allocation

### Recent (2018-2026)

**Mulliner, A., Harvey, C. R., Xia, C., Fang, E., & Van Hemert, O. (2025). Regimes.** *The Journal of Portfolio Management* 52(4):6-25. DOI 10.3905/jpm.2025.1.798. SSRN version DOI 10.2139/ssrn.5164863. [CR] `mulliner2025regimes`
- Similarity-based regime identification: z-scored annual changes in seven state variables (S&P 500, yield-curve slope, oil, copper, T-bill yield, equity vol, stock-bond correlation), find the historically most similar dates, trade on what followed. Tested on six long-short equity factors, 1985-2024 (per secondary summaries; not read in full).
- Relevance: a non-HMM, non-parametric regime approach from a large practitioner group. Sample is 40 years and the target is factors, so it does not cover the 100-year stocks/bonds/cash question.

**Nystrup, P., Lindström, E., & Madsen, H. (2020). Learning hidden Markov models with persistent states by penalizing jumps.** *Expert Systems with Applications* 150:113307. DOI 10.1016/j.eswa.2020.113307. [CR] `nystrup2020penalizing`
- Brings the Bemporad et al. (2018) jump-model estimator into finance: cluster temporal features and penalize state changes, so persistence is controlled directly instead of through an estimated transition matrix. Compared against ML-estimated HMMs and spectral clustering in simulation and on financial data; more persistent states reduced trading costs in a trading example (per seminar synopses; journal abstract not read).

**Nystrup, P., Kolm, P. N., & Lindström, E. (2020). Greedy online classification of persistent market states using realized intraday volatility features.** *The Journal of Financial Data Science* 2(3):25-39. DOI 10.3905/jfds.2020.2.3.025. [CR] `nystrup2020greedy`

**Nystrup, P., Madsen, H., & Lindström, E. (2018). Dynamic portfolio optimization across hidden market regimes.** *Quantitative Finance* 18(1):83-95. DOI 10.1080/14697688.2017.1342857. (Crossref issued 2017 online.) [CR] `nystrup2018dynamic`
- HMM with time-varying parameters feeding a model-predictive-control (MPC) allocator with transaction costs. One of the few papers that couples a regime filter with a cost-aware multi-period optimizer.

**Nystrup, P., Hansen, B. W., Larsen, H. O., Madsen, H., & Lindström, E. (2018). Dynamic allocation or diversification: A regime-based approach to multiple assets.** *The Journal of Portfolio Management* 44(2):62-73. DOI 10.3905/jpm.2018.44.2.062. (Crossref issued Dec 2017 online.) [CR] `nystrup2018diversification`

**Nystrup, P., Madsen, H., & Lindström, E. (2017). Long memory of financial time series and hidden Markov models with time-varying parameters.** *Journal of Forecasting* 36(8):989-1002. DOI 10.1002/for.2447. [CR] `nystrup2017longmemory`

**Nystrup, P., Hansen, B. W., Madsen, H., & Lindström, E. (2016). Detecting change points in VIX and S&P 500: A new approach to dynamic asset allocation.** *Journal of Asset Management* 17(5):361-374. DOI 10.1057/jam.2016.12. [CR] `nystrup2016changepoints`

**Nystrup, P., Hansen, B. W., Madsen, H., & Lindström, E. (2015). Regime-based versus static asset allocation: Letting the data speak.** *The Journal of Portfolio Management* 42(1):103-109. DOI 10.3905/jpm.2015.42.1.103. [CR] `nystrup2015regimebased`

**Kinlaw, W. B., Kritzman, M., Metcalfe, M., & Turkington, D. (2023). The determinants of inflation.** Journal of Investment Management (2023) per secondary sources. SSRN DOI 10.2139/ssrn.4137861 [CR for SSRN only]. Journal volume/issue/pages UNVERIFIED.
- HMM inflation regimes on 1960-2022 data. Listed for the Kritzman line of work.

### Classic anchors

**Hamilton, J. D. (1989). A new approach to the economic analysis of nonstationary time series and the business cycle.** *Econometrica* 57(2):357-384. DOI 10.2307/1912559. JSTOR https://www.jstor.org/stable/1912559. [CR; Crossref lists start page 357 only, end page 384 is the standard citation] `hamilton1989`

**Turner, C. M., Startz, R., & Nelson, C. R. (1989). A Markov model of heteroskedasticity, risk, and learning in the stock market.** *Journal of Financial Economics* 25(1):3-22. DOI 10.1016/0304-405X(89)90094-9. [CR] `turner1989markov`

**Ang, A., & Bekaert, G. (2002). International asset allocation with regime shifts.** *Review of Financial Studies* 15(4):1137-1187. DOI 10.1093/rfs/15.4.1137. [CR] `ang2002international`

**Ang, A., & Bekaert, G. (2002). Regime switches in interest rates.** *Journal of Business & Economic Statistics* 20(2):163-182. DOI 10.1198/073500102317351930. [CR] `ang2002interest`

**Ang, A., & Bekaert, G. (2004). How regimes affect asset allocation.** *Financial Analysts Journal* 60(2):86-99. DOI 10.2469/faj.v60.n2.2612. NBER WP 10080 (DOI 10.3386/w10080). [CR] `ang2004regimes`
- Regime-switching strategy dominates static out of sample for all-equity international portfolios; when cash and bonds are allowed, a persistent bear regime moves the investor mainly into cash. OOS window in the NBER version is 1985-2000 (15 years).

**Guidolin, M., & Timmermann, A. (2007). Asset allocation under multivariate regime switching.** *Journal of Economic Dynamics and Control* 31(11):3503-3544. DOI 10.1016/j.jedc.2006.12.004. [CR] `guidolin2007asset`
- Four regimes (crash, slow growth, bull, recovery) for joint stock/bond returns; OOS forecasting experiments confirm economic value.

**Guidolin, M., & Timmermann, A. (2008). International asset allocation under regime switching, skew, and kurtosis preferences.** *Review of Financial Studies* 21(2):889-935. DOI 10.1093/rfs/hhn006. [CR] `guidolin2008international`

**Tu, J. (2010). Is regime switching in stock returns important in portfolio decisions?** *Management Science* 56(7):1198-1215. DOI 10.1287/mnsc.1100.1181. [CR] `tu2010regime`

**Pettenuzzo, D., & Timmermann, A. (2011). Predictability of stock returns and asset allocation under structural breaks.** *Journal of Econometrics* 164(1):60-78. DOI 10.1016/j.jeconom.2011.02.019. [CR] `pettenuzzo2011breaks`
- A corrigendum exists: Pettenuzzo, Song & Timmermann (2022), *J. Econometrics* 227(2):513-517, DOI 10.1016/j.jeconom.2020.02.008. [CR] Cite both if you use this paper.

**Bulla, J., Mergner, S., Bulla, I., Sesboüé, A., & Chesneau, C. (2011). Markov-switching asset allocation: Do profitable strategies exist?** *Journal of Asset Management* 12(5):310-321. DOI 10.1057/jam.2010.27. [CR] `bulla2011markov`
- Daily equity indices (US, Germany, Japan), ~40 years; HMM switching profitable OOS after costs. This is the direct ancestor of the Shu-Yu-Mulvey design (same three markets).

**Ang, A., & Timmermann, A. (2012). Regime changes and financial markets.** *Annual Review of Financial Economics* 4(1):313-337. DOI 10.1146/annurev-financial-110311-101808. NBER WP 17182. [CR] `ang2012regime`

**Kritzman, M., Page, S., & Turkington, D. (2012). Regime shifts: Implications for dynamic strategies (corrected).** *Financial Analysts Journal* 68(3):22-39. DOI 10.2469/faj.v68.n3.3. [CR] `kritzman2012regime`
- Two-state Markov-switching models on turbulence, inflation, and economic growth; regime forecasts scale risk-premium exposures and drive stock/bond/cash allocation; dynamic beats static, especially for loss-averse investors.
- Open question to check in the full text: whether the growth and inflation regimes use first-release (vintage) macro data or revised data. The abstract does not say.

**Bae, G. I., Kim, W. C., & Mulvey, J. M. (2014). Dynamic asset allocation for varied financial markets under regime switching framework.** *European Journal of Operational Research* 234(2):450-458. DOI 10.1016/j.ejor.2013.03.032. [CR] `bae2014dynamic`

---

## 2. Statistical jump models (current state of the art)

### Method papers

**Bemporad, A., Breschi, V., Piga, D., & Boyd, S. P. (2018). Fitting jump models.** *Automatica* 96:11-21. DOI 10.1016/j.automatica.2018.06.022. [CR] `bemporad2018fitting`
- The estimator underlying all of the finance jump-model work: alternate between fitting per-state parameters and a Viterbi-style state sequence with a fixed penalty per jump.

**Nystrup, P., Kolm, P. N., & Lindström, E. (2021). Feature selection in jump models.** *Expert Systems with Applications* 184:115558. DOI 10.1016/j.eswa.2021.115558. [CR] `nystrup2021feature`
- Introduces the sparse jump model (feature weights with an L1-type constraint, alternating with state estimation).

**Aydınhan, A. O., Kolm, P. N., Mulvey, J. M., & Shu, Y. (2024). Identifying patterns in financial markets: Extending the statistical jump model for regime identification.** *Annals of Operations Research*, online first 14 May 2024. DOI 10.1007/s10479-024-06035-z. SSRN 4556048 (DOI 10.2139/ssrn.4556048). [CR] `aydinhan2024identifying`
- Volume/issue/pages: not assigned in Crossref or OpenAlex as of 2026-10-08. Cite as online first with DOI.
- Earlier working title: "Continuous Statistical Jump Models for Identifying Financial Regimes."
- Contribution: generalizes the hard state to a probability vector over regimes (the continuous jump model, CJM) and adds a "mode loss" penalty pushing probabilities toward simplex vertices. Claims outperformance over HMMs, largest when regimes are imbalanced and data are short.
- Empirics (per abstract-level summaries; full text not read): daily returns of major US, German and Japanese equity indices over ~40 years; OOS strategy profitable after transaction costs. Hyperparameter-selection protocol: UNVERIFIED from full text.
- POMDP relevance: the CJM output is the closest thing in this literature to a belief state, but it comes from penalized clustering rather than from a Bayesian filter.

**Cortese, F. P., Kolm, P. N., & Lindström, E. (2023). What drives cryptocurrency returns? A sparse statistical jump model approach.** *Digital Finance* 5(3-4):483-518. DOI 10.1007/s42521-023-00085-x. [CR] `cortese2023crypto`

**Cortese, F. P., Kolm, P. N., & Lindström, E. (2026). Generalized information criteria for high-dimensional sparse statistical jump models.** *AStA Advances in Statistical Analysis* 110(2):289-317. DOI 10.1007/s10182-026-00554-9. SSRN 4774429. [CR] `cortese2026gic`
- Model selection (number of states, sparsity, jump penalty) via generalized information criteria instead of strategy-Sharpe cross-validation. Empirical application: three-state model for MSCI developed and EM indices. This is the main alternative to the "tune lambda on backtest Sharpe" practice criticized below.

### Allocation papers (newest first)

**Luo, Y., & Mulvey, J. M. (2026). Regime-aware asset allocation with dual-regime signals and regime-dependent asset selection.** SSRN working paper, DOI 10.2139/ssrn.6933278. [CR existence only; content not read] `luo2026dualregime`

**Luo, Y., & Mulvey, J. M. (2026). Regime-aware reinforcement learning: A mixture-of-experts framework for dynamic asset allocation.** SSRN working paper, DOI 10.2139/ssrn.7038299. [CR existence only; content not read] `luo2026moe`

**Li, X., Chen, J., Tao, X., & Ji, Y. (2025). Regime-switching asset allocation using a framework combing [sic] a jump model and model predictive control.** *Mathematics* 13(17):2837. DOI 10.3390/math13172837. [CR] `li2025jmmpc`
- JM regimes feed rolling multi-horizon return/covariance estimates into an MPC allocator; reported to beat equal weight with smaller drawdowns.
- Vulnerability (UNVERIFIED, from a search-engine summary of the full text; MDPI blocked my fetch): hyperparameters reportedly chosen by running OOS backtests over the historical data and keeping the configuration with the highest Sharpe. If confirmed, the reported Sharpe is selected on the evaluation period. Rolling window reported as 1,000 observations (~3 years).

**Shu, Y., & Mulvey, J. M. (2025). Dynamic factor allocation leveraging regime-switching signals.** *The Journal of Portfolio Management* 51(3):50-72 (Crossref print date 31 Dec 2024; volume 51 is the 2025 volume). DOI 10.3905/jpm.2024.1.649. arXiv 2410.14841. [CR, AX, READ] `shu2025factor`
- Data: Bloomberg daily total returns, Jan 1993 to Jun 2024, for seven long-only US indices (MSCI USA, Enhanced Value, Low Size, Momentum, Quality, Min Vol, Russell 1000 Growth). Market features from FRED (VIX, 2y yield, 10y-2y).
- OOS test: 2007-2024. Sparse JM refit monthly on an expanding window of 8 to 12 years; online inference between refits.
- Hyperparameters (jump penalty lambda, sparsity kappa): chosen per factor on a 6-year validation window that rolls forward every 6 months; criterion is the Sharpe of a long-short single-factor strategy. Validation precedes the period it is applied to. Grid not stated in what I read.
- Costs: 5 bps per side; one-day delay (signal at T applied on T+2).
- Headline: active IR vs market rises from 0.05 (equal-weight factors) to roughly 0.24-0.44 depending on tracking-error budget (1-4%); vs EW benchmark, IR 0.40-0.49. Absolute Sharpe 0.57-0.65 vs 0.52 market; max drawdown about -50.5% to -52.5% vs -54.9% market. Turnover 237-628% one-way per year.
- Vulnerabilities: OOS period is a single 17-year window; the tracking-error sweep is shown on the same test period; absolute drawdown is barely changed because the portfolio stays fully invested; high turnover against a 5 bp cost assumption; FRED series used without vintage control (the authors call them real-time accessible but do not address revisions); feature standardization method not described.

**Shu, Y., Yu, C., & Mulvey, J. M. (2025). Dynamic asset allocation with asset-specific regime forecasts.** *Annals of Operations Research* 346(1):285-318 (print March 2025; online 26 Sep 2024). DOI 10.1007/s10479-024-06266-0. arXiv 2406.09578. [CR, AX, READ] `shu2024assetspecific`
- Data: Bloomberg daily USD total-return indices 1991-2023 for 12 assets (US large/mid/small cap, EAFE, EM, US Agg, long Treasury, high yield, IG corporate, REIT, commodities, gold); 3m T-bill (FRED); macro features (2y yield, 10y-2y slope, VIX, stock-bond correlation).
- Design: JM labels historical regimes per asset; an XGBoost classifier (default hyperparameters) forecasts next-day regime from return plus macro features; forecasts feed min-variance, mean-variance and EW optimizers (long-only, 40% cap).
- OOS: 2007-2023. JM and XGBoost refit every 6 months on an 11-year lookback. Jump penalty chosen per asset every 6 months on a log grid over [0, 100], by Sharpe of a 0/1 strategy on the preceding 5-year validation window.
- Selection on non-OOS data: the probability-smoothing halflife was chosen on a single 2002-2007 validation window; dropping downside-deviation features for AggBond, Treasury and Gold was based on "preliminary in-sample analysis" with no window stated.
- Costs: 5 bps one-way, plus a trading penalty in the optimizer. Execution delay: not stated in the parts I read.
- Headline (2007-2023, net): MinVar Sharpe 0.70 to 1.12 (MDD -19.3% to -7.1%); MV 0.37 to 1.02; EW 0.51 to 0.91 (MDD -37.5% to -17.6%); 60/40 0.57 (MDD -31.5%). Single-asset S&P 500 0/1: Sharpe 0.50 to 0.79, MDD -55% to -18%. Turnover up to 11.7x/yr for EW (JM-XGB).
- Vulnerabilities: one test window dominated by 2008 and 2020; the MV baseline uses a deliberately naive return estimate (the authors say so); no HMM comparison in the results; high turnover at a 5 bp cost assumption; one passage says data begin in 2002, conflicting with the 1991 start stated elsewhere.

**Shu, Y., Yu, C., & Mulvey, J. M. (2024). Downside risk reduction using regime-switching signals: A statistical jump model approach.** *Journal of Asset Management* 25(5):493-507. DOI 10.1057/s41260-024-00376-x. arXiv 2402.05272 (v1 titled "Regime-Aware Asset Allocation: a Statistical Jump Model Approach"). [CR, AX, READ] `shu2024downside`
- Data: Bloomberg daily total returns for S&P 500, DAX, Nikkei 225 (local currency, each tested separately); 3m bill yields from Global Financial Data. Full sample 1970-2023.
- OOS: 1990-2023 (12-year training + 8-year validation burn-in). JM refit every 6 months on a rolling 3,000-day window; daily online inference. HMM benchmark refit daily on 3,000 days.
- Jump penalty: chosen monthly during the OOS period, as the candidate with the highest Sharpe of the 0/1 strategy over the preceding 8-year validation window. Validation precedes trading. Candidate grid not specified in the text I read.
- Costs: 10 bps one-way. Delay: 1 day by default (signal at end of t, trade from t+2); 5- and 10-day delays tested.
- Allocation: binary, 100% index or 100% T-bills.
- Features: EWM downside deviation (10-day halflife) and EWM Sortino ratios (20, 60 days) on excess returns. All trailing. Standardization method not described.
- Headline (1990-2023, net): Sharpe / MDD. S&P 500: buy-and-hold 0.48 / -55.2%, HMM 0.54 / -28.9%, JM 0.68 / -26.6%. DAX: 0.30 / -72.7%, 0.35 / -40.5%, 0.44 / -39.4%. Nikkei: 0.12 / -79.1%, 0.19 / -48.6%, 0.31 / -45.3%. CAGR JM vs B&H: 11.2% vs 10.2% (US), 8.6% vs 6.8% (DE), 4.7% vs 0.8% (JP).
- Authors' own caveats: detection lag of roughly half a month; misclassification in choppy turbulent periods; 0/1 switching "may be too extreme" for practice; two states, three indices.

**Shu, Y. (2025). Princeton PhD dissertation on statistical jump models** ("Modeling Regime Changes in Financial Markets Using Statistical Jump Models: Methodology and Applications"), Princeton DataSpace handle 88435/dsp01g158bm716. UNVERIFIED (the record returned HTTP 401 to my fetch; title taken from the search index only).

### What the strongest jump-model papers claim, and where they are exposed

Claims:
1. JM regimes are more persistent than HMM regimes, so a 0/1 or tilt strategy trades less and is less whipsawed.
2. Out of sample with walk-forward penalty selection, costs, and a one-day delay, JM switching roughly halves max drawdown and raises Sharpe by about 0.1-0.2 on major equity indices (1990-2023), and lifts multi-asset Sharpe substantially (2007-2023).
3. Feeding JM labels into a supervised forecaster (XGBoost) or Black-Litterman views transfers the signal into multi-asset and factor portfolios.

Exposures:
- **Sample length and composition.** OOS windows are 34 years (equity only) or 17 years (multi-asset, factors). Both contain 2000-02, 2008 and 2020, which are exactly the episodes drawdown-avoidance strategies are built to catch. No pre-1990 OOS evidence, no inflationary-bear episode like 1973-74 in OOS for the multi-asset work, no 1929-32 or 1937-38.
- **Hyperparameter selection.** The jump penalty is tuned walk-forward, which is genuinely better than most of the literature. Many other choices (feature families, halflives, number of states = 2, training/validation lengths, smoothing halflife, dropped features, grid bounds) were fixed with the full sample visible, and some were fixed on a named in-sample window. None of the three papers reports a multiple-testing correction (PBO, deflated Sharpe, White/Hansen SPA). I did not see significance tests for the Sharpe differences in the sections I read; check before claiming they are absent.
- **Costs.** 5-10 bps one-way on index total returns, with turnover up to 6x (factor paper) and 11.7x (EW multi-asset). For 1990s DAX/Nikkei futures or cash baskets, and for REIT/HY/EM sleeves, those numbers are optimistic. No cost sensitivity curve beyond delay tests in the 2024 equity paper.
- **Look-ahead.** Price-based features are trailing. Feature standardization is unspecified in two of the three papers (full-sample z-scoring would leak). Macro features come from FRED with no vintage control. Regime labels used to train XGBoost come from smoothed (full-window) JM fits inside each training window, which is fine as long as the training window ends before the forecast date; the papers state that it does.
- **Benchmarks.** Comparisons are to buy-and-hold, an HMM, 60/40, and naive optimizers. None of the papers runs a horse race against the obvious cheap baselines under the identical protocol: a 10-month SMA rule (Faber 2007), 12-month TSMOM, or volatility targeting.

---

## 3. Volatility timing and its critiques

**DeMiguel, V., Martín-Utrera, A., & Uppal, R. (2024). A multifactor perspective on volatility-managed portfolios.** *The Journal of Finance* 79(6):3859-3891. DOI 10.1111/jofi.13395. [CR] `demiguel2024multifactor`
- Strongest recent pro-timing result: a conditional multifactor mean-variance portfolio whose factor weights shrink with market volatility outperforms its unconditional counterpart out of sample and net of costs. It answers Cederburg et al. by timing the multifactor portfolio jointly instead of each factor separately.

**Wang, F., & Yan, X. S. (2021). Downside risk and the performance of volatility-managed portfolios.** *Journal of Banking & Finance* 131:106198. DOI 10.1016/j.jbankfin.2021.106198. [CR] `wang2021downside`
- Scaling by downside volatility works better than by total volatility; fixed-weight combinations help real-time investors.

**Barroso, P., & Detzel, A. (2021). Do limits to arbitrage explain the benefits of volatility-managed portfolios?** *Journal of Financial Economics* 140(3):744-767. DOI 10.1016/j.jfineco.2021.02.009. [CR] `barroso2021limits`
- After transaction costs (six cost-mitigation methods), volatility management of factors other than the market yields zero abnormal returns and lower Sharpe ratios. The volatility-managed **market** portfolio survives costs; its gains are concentrated in high-sentiment periods.

**Cederburg, S., O'Doherty, M. S., Wang, F., & Yan, X. S. (2020). On the performance of volatility-managed portfolios.** *Journal of Financial Economics* 138(1):95-117. DOI 10.1016/j.jfineco.2020.04.015. [CR, READ abstract and introduction from the published PDF] `cederburg2020performance`
- 103 equity strategies. Managed portfolios do not systematically beat unmanaged ones in direct Sharpe comparisons. Spanning-regression alphas are positive (replicating Moreira-Muir), but exploiting them needs ex post optimal weights on the managed and unmanaged legs. Feasible real-time versions usually earn lower CER and Sharpe than the unmanaged portfolio. Cause: structural instability in the spanning regressions.

**Liu, F., Tang, X., & Zhou, G. (2019). Volatility-managed portfolio: Does it really work?** *The Journal of Portfolio Management* 46(1):38-51. DOI 10.3905/jpm.2019.1.107. [CR] `liu2019volatility`
- The standard market application has look-ahead bias: the scaling constant c is set with full-sample volatility. After correction, max drawdowns are 68%-93% in almost all cases and outperformance is confined to the financial-crisis period.

**Moreira, A., & Muir, T. (2019). Should long-term investors time volatility?** *Journal of Financial Economics* 131(3):507-527. DOI 10.1016/j.jfineco.2018.09.011. [CR] `moreira2019longterm`
- A long-horizon investor ignoring volatility variation loses the equivalent of 2.4% of wealth per year (published abstract). This is a calibrated model result, which differs from a real-time backtest.

**Harvey, C. R., Hoyle, E., Korgaonkar, R., Rattray, S., Sargaison, M., & Van Hemert, O. (2018). The impact of volatility targeting.** *The Journal of Portfolio Management* 45(1):14-33. DOI 10.3905/jpm.2018.45.1.014. [CR] `harvey2018voltarget`
- 60+ assets, daily data from as early as 1926. Vol targeting raises Sharpe for risk assets (equities, credit) and for 60/40, reduces max drawdown for balanced and risk-parity portfolios, and has little effect on bonds/FX/commodities. Closest thing to a century-scale real-time-style risk-management test, but it is volatility scaling, with no regime model involved.

**Bongaerts, D., Kang, X., & van Dijk, M. (2020). Conditional volatility targeting.** *Financial Analysts Journal* 76(4):54-71. DOI 10.1080/0015198X.2020.1790853. [CR] `bongaerts2020conditional`

**Moreira, A., & Muir, T. (2017). Volatility-managed portfolios.** *The Journal of Finance* 72(4):1611-1644. DOI 10.1111/jofi.12513. NBER WP 22208. [CR] `moreira2017volatility`
- Managed portfolios that cut risk when recent realized variance is high produce large alphas, higher Sharpe ratios, and large mean-variance utility gains across many factors.

**Fleming, J., Kirby, C., & Ostdiek, B. (2003). The economic value of volatility timing using "realized" volatility.** *Journal of Financial Economics* 67(3):473-509. DOI 10.1016/S0304-405X(02)00259-3. [CR] `fleming2003realized`
- Source of the "willing to pay 50-200 bps per year" figure (often misattributed to the 2001 paper).

**Fleming, J., Kirby, C., & Ostdiek, B. (2001). The economic value of volatility timing.** *The Journal of Finance* 56(1):329-352. DOI 10.1111/0022-1082.00327. [CR] `fleming2001economic`
- Short-horizon mean-variance investor across stocks, bonds and gold (whether cash is included: check full text); volatility-timing beats static efficient portfolios with the same target return and vol, robust to estimation risk.

### What the strongest volatility-timing papers claim, and where they are exposed

- **Moreira & Muir (2017):** positive alphas from spanning regressions across factors. Exposed on implementability (Cederburg et al.: the alpha needs ex post combination weights; real-time versions lose), on the scaling constant (Liu-Tang-Zhou: full-sample c is look-ahead), and on costs (Barroso-Detzel: gone for every factor except the market).
- **What survives:** the managed *market* portfolio after costs (Barroso-Detzel), downside-vol scaling (Wang-Yan), and joint multifactor conditioning (DeMiguel et al. 2024). Harvey et al. (2018) show the risk-reduction benefit for equities and 60/40 over long samples.
- **Remaining exposures:** leverage is required in calm periods (the strategy's mean-return gain comes partly from levering up low-vol months, which a stocks/bonds/cash allocator with a 100% cap cannot do); Liu-Tang-Zhou find outperformance concentrated in 2008; most evidence is post-1926 US equity. For your paper the clean comparison is a capped (0-100% equity) volatility rule, which removes the leverage channel and leaves pure de-risking, i.e. the same action space as a regime switcher.

---

## 4. Trend / time-series momentum

**Huang, D., Li, J., Wang, L., & Zhou, G. (2020). Time series momentum: Is it there?** *Journal of Financial Economics* 135(3):774-794. DOI 10.1016/j.jfineco.2019.08.004. [CR] `huang2020tsmom`
- Asset-by-asset regressions show little TSMOM in or out of sample; the pooled t-statistic fails bootstrap critical values; TSMOM performs about the same as a historical-mean strategy (TSH) that needs no predictability. Also flags look-ahead from time-series demeaning in pooled regressions.

**Hurst, B., Ooi, Y. H., & Pedersen, L. H. (2017). A century of evidence on trend-following investing.** *The Journal of Portfolio Management* 44(1):15-29. DOI 10.3905/jpm.2017.44.1.015. [CR] `hurst2017century`
- 1880-2016, 67 markets (per AQR summary); 1/3/12-month trend positive in every decade after simulated 2/20 fees. Authors are AQR principals. Lookbacks were chosen with the modern literature in view, so the pre-1985 portion is out of sample only in the sense that the data predate the idea.

**Lempérière, Y., Deremble, C., Seager, P., Potters, M., & Bouchaud, J.-P. (2014). Two centuries of trend following.** *The Journal of Investment Strategies* 3(3):41-61. DOI 10.21314/JOIS.2014.043. [CR] `lemperiere2014two`

**Levine, A., & Pedersen, L. H. (2016). Which trend is your friend?** *Financial Analysts Journal* 72(3):51-66. DOI 10.2469/faj.v72.n3.3. [CR] `levine2016trend`

**Kim, A. Y., Tse, Y., & Wald, J. K. (2016). Time series momentum and volatility scaling.** *Journal of Financial Markets* 30:103-124. DOI 10.1016/j.finmar.2016.05.003. [CR] `kim2016tsmom`
- Argues TSMOM profits come largely from volatility scaling. Links clusters 3 and 4.

**Goyal, A., & Jegadeesh, N. (2018). Cross-sectional and time-series tests of return predictability: What is the difference?** *Review of Financial Studies* 31(5):1784-1824. DOI 10.1093/rfs/hhx131. (Crossref issued 2017 online.) [CR] `goyal2018tsmom`

**Moskowitz, T. J., Ooi, Y. H., & Pedersen, L. H. (2012). Time series momentum.** *Journal of Financial Economics* 104(2):228-250. DOI 10.1016/j.jfineco.2011.11.003. [CR] `moskowitz2012tsmom`
- TSMOM in all 58 liquid futures/forwards studied (equity indices, currencies, commodities, bonds).

**Faber, M. T. (2007). A quantitative approach to tactical asset allocation.** *The Journal of Wealth Management* 9(4):69-79. DOI 10.3905/jwm.2007.674809. [CR] `faber2007quantitative`
- 10-month SMA in/out rule. The natural zero-parameter-tuning baseline for any regime switcher.

**Zakamulin, V. (2017). Market Timing with Moving Averages: The Anatomy and Performance of Trading Rules.** Palgrave Macmillan / Springer. DOI 10.1007/978-3-319-60970-6. [CR] `zakamulin2017book`
- Long-sample (S&P Composite from 1860) MA timing, with data-snooping-aware testing; reports weaker evidence post-1932 (per secondary summaries).

---

## 5. Look-ahead, real-time data, backtest overfitting

**Goyal, A., Welch, I., & Zafirov, A. (2024). A comprehensive 2022 look at the empirical performance of equity premium prediction.** *Review of Financial Studies* 37(11):3490-3557. DOI 10.1093/rfs/hhae044. SSRN 3929119. [CR] `goyal2024comprehensive`

**Arnott, R., Harvey, C. R., & Markowitz, H. (2019). A backtesting protocol in the era of machine learning.** *The Journal of Financial Data Science* 1(1):64-74. DOI 10.3905/jfds.2019.1.064. [CR] `arnott2019protocol`

**Bailey, D. H., Borwein, J. M., López de Prado, M., & Zhu, Q. J. (2017). The probability of backtest overfitting.** *Journal of Computational Finance* 20(4):39-69. DOI 10.21314/JCF.2016.322 (online 19 Sep 2016). [CR + WEB: Risk.net article page] `bailey2017pbo`

**Bailey, D. H., Borwein, J. M., López de Prado, M., & Zhu, Q. J. (2014). Pseudo-mathematics and financial charlatanism: The effects of backtest overfitting on out-of-sample performance.** *Notices of the American Mathematical Society* 61(5):458-471. DOI 10.1090/noti1105. [CR for start page; full range 458-471 confirmed in the Borwein memorial bibliography, arXiv 2107.06030] `bailey2014pseudo`

**Bailey, D. H., & López de Prado, M. (2014). The deflated Sharpe ratio: Correcting for selection bias, backtest overfitting, and non-normality.** *The Journal of Portfolio Management* 40(5):94-107. DOI 10.3905/jpm.2014.40.5.094. [CR] `bailey2014deflated`

**Harvey, C. R., Liu, Y., & Zhu, H. (2016). ... and the cross-section of expected returns.** *Review of Financial Studies* 29(1):5-68. DOI 10.1093/rfs/hhv059. (Crossref issued 2015 online.) [CR] `harvey2016cross`

**Harvey, C. R., & Liu, Y. (2015). Backtesting.** *The Journal of Portfolio Management* 42(1):13-28. DOI 10.3905/jpm.2015.42.1.013. [CR] `harvey2015backtesting`

**McLean, R. D., & Pontiff, J. (2016). Does academic research destroy stock return predictability?** *The Journal of Finance* 71(1):5-32. DOI 10.1111/jofi.12365. [CR] `mclean2016academic`

**Croushore, D. (2011). Frontiers of real-time data analysis.** *Journal of Economic Literature* 49(1):72-100. DOI 10.1257/jel.49.1.72. [CR] `croushore2011frontiers`

**Rapach, D. E., Strauss, J. K., & Zhou, G. (2010). Out-of-sample equity premium prediction: Combination forecasts and links to the real economy.** *Review of Financial Studies* 23(2):821-862. DOI 10.1093/rfs/hhp063. [CR] `rapach2010combination`

**Welch, I., & Goyal, A. (2008). A comprehensive look at the empirical performance of equity premium prediction.** *Review of Financial Studies* 21(4):1455-1508. DOI 10.1093/rfs/hhm014. [CR] `welch2008comprehensive`

**Campbell, J. Y., & Thompson, S. B. (2008). Predicting excess stock returns out of sample: Can anything beat the historical average?** *Review of Financial Studies* 21(4):1509-1531. DOI 10.1093/rfs/hhm055. [CR] `campbell2008predicting`

**Hansen, P. R. (2005). A test for superior predictive ability.** *Journal of Business & Economic Statistics* 23(4):365-380. DOI 10.1198/073500105000000063. [CR] `hansen2005spa`

**Hsu, P.-H., & Kuan, C.-M. (2005). Reexamining the profitability of technical analysis with data snooping checks.** *Journal of Financial Econometrics* 3(4):606-628. DOI 10.1093/jjfinec/nbi026. [CR; Crossref lists only the first author, second author from the SSRN version] `hsu2005reexamining`

**Croushore, D., & Stark, T. (2001). A real-time data set for macroeconomists.** *Journal of Econometrics* 105(1):111-130. DOI 10.1016/S0304-4076(01)00072-0. [CR] `croushore2001realtime`
- Dataset: Federal Reserve Bank of Philadelphia, Real-Time Data Set for Macroeconomists (RTDSM), monthly-updated vintages of major macro series. https://www.philadelphiafed.org/surveys-and-data/real-time-data-research/real-time-data-set-for-macroeconomists [WEB]. The Fed asks that technical work cite Croushore & Stark (2001).

**White, H. (2000). A reality check for data snooping.** *Econometrica* 68(5):1097-1126. DOI 10.1111/1468-0262.00152. [CR] `white2000reality`

**Pesaran, M. H., & Timmermann, A. (1995). Predictability of stock returns: Robustness and economic significance.** *The Journal of Finance* 50(4):1201-1228. DOI 10.1111/j.1540-6261.1995.tb04055.x. [CR] `pesaran1995predictability`
- Early recursive "real-time investor" design: the model search itself is repeated each period with only past data. This is the template for a strictly real-time regime-model evaluation.

Long-history data sources (useful for a 100-year study):
- **Jordà, Ò., Knoll, K., Kuvshinov, D., Schularick, M., & Taylor, A. M. (2019). The rate of return on everything, 1870-2015.** *Quarterly Journal of Economics* 134(3):1225-1298. DOI 10.1093/qje/qjz012. [CR] `jorda2019rate` (annual frequency only)
- **Golez, B., & Koudijs, P. (2018). Four centuries of return predictability.** *Journal of Financial Economics* 127(2):248-263. DOI 10.1016/j.jfineco.2017.12.007. [CR] `golez2018four`

---

## 6. Transaction costs and no-trade regions

**Collin-Dufresne, P., Daniel, K., & Sağlam, M. (2020). Liquidity regimes and optimal dynamic asset allocation.** *Journal of Financial Economics* 136(2):379-406. DOI 10.1016/j.jfineco.2019.09.011. [CR] `collindufresne2020liquidity`
- Gârleanu-Pedersen with regime-switching returns *and* regime-dependent trading costs. The closest published model to "optimal trading on a hidden-Markov signal with costs"; regimes are observed in the main model, so it is an MDP rather than a POMDP.

**Nystrup, P., Boyd, S., Lindström, E., & Madsen, H. (2019). Multi-period portfolio selection with drawdown control.** *Annals of Operations Research* 282(1-2):245-271. DOI 10.1007/s10479-018-2947-3. (Crossref issued 2018 online.) [CR] `nystrup2019drawdown`
- HMM-based forecasts plus MPC with transaction costs and drawdown control. Empirical cost-aware regime allocation.

**Boyd, S., Busseti, E., Diamond, S., Kahn, R. N., Koh, K., Nystrup, P., & Speth, J. (2017). Multi-period trading via convex optimization.** *Foundations and Trends in Optimization* 3(1):1-76. DOI 10.1561/2400000023. [CR; author order follows the publication, Crossref lists the same seven authors in a different order] `boyd2017multiperiod`

**Gârleanu, N., & Pedersen, L. H. (2013). Dynamic trading with predictable returns and transaction costs.** *The Journal of Finance* 68(6):2309-2340. DOI 10.1111/jofi.12080. [CR] `garleanu2013dynamic`
- "Aim in front of the target, trade partially toward it." Quadratic costs, linear factor dynamics; persistent signals get more weight. Regime probabilities from a filter are a natural slow-moving signal in this framework.

**Lynch, A. W., & Tan, S. (2010). Multiple risky assets, transaction costs, and return predictability: Allocation rules and implications for U.S. investors.** *Journal of Financial and Quantitative Analysis* 45(4):1015-1053. DOI 10.1017/S0022109010000360. [CR] `lynch2010multiple`

**Jang, B.-G., Koo, H. K., Liu, H., & Loewenstein, M. (2007). Liquidity premia and transaction costs.** *The Journal of Finance* 62(5):2329-2366. DOI 10.1111/j.1540-6261.2007.01277.x. [CR] `jang2007liquidity`
- Proportional costs with regime-switching investment opportunities: the no-trade region shifts with the regime, and liquidity premia can be first order. Directly relevant to a belief-dependent no-trade band.

**Liu, H. (2004). Optimal consumption and investment with transaction costs and multiple risky assets.** *The Journal of Finance* 59(1):289-338. DOI 10.1111/j.1540-6261.2004.00634.x. [CR] `liu2004optimal`

**Rogers, L. C. G. (2004). Why is the effect of proportional transaction costs O(δ^{2/3})?** In G. Yin & Q. Zhang (Eds.), *Mathematics of Finance*, Contemporary Mathematics vol. 351, pp. 303-308. American Mathematical Society. DOI 10.1090/conm/351/06411. [CR + WEB] `rogers2004why`

**Lynch, A. W., & Balduzzi, P. (2000). Predictability and transaction costs: The impact on rebalancing rules and behavior.** *The Journal of Finance* 55(5):2285-2309. DOI 10.1111/0022-1082.00287. [CR] `lynch2000predictability`

**Balduzzi, P., & Lynch, A. W. (1999). Transaction costs and predictability: Some utility cost calculations.** *Journal of Financial Economics* 52(1):47-78. DOI 10.1016/S0304-405X(99)00004-5. [CR; Crossref lists only the first author] `balduzzi1999transaction`

**Shreve, S. E., & Soner, H. M. (1994). Optimal investment and consumption with transaction costs.** *The Annals of Applied Probability* 4(3):609-692. DOI 10.1214/aoap/1177004966. [CR + WEB: Project Euclid] `shreve1994optimal`
- Appendix shows the value-function loss scales as cost^{2/3}.

**Davis, M. H. A., & Norman, A. R. (1990). Portfolio selection with transaction costs.** *Mathematics of Operations Research* 15(4):676-713. DOI 10.1287/moor.15.4.676. [CR] `davis1990portfolio`

**Magill, M. J. P., & Constantinides, G. M. (1976). Portfolio selection with transactions costs.** *Journal of Economic Theory* 13(2):245-263. DOI 10.1016/0022-0531(76)90018-1. [CR] `magill1976portfolio`

Hidden-Markov signal plus costs, in one place: Collin-Dufresne et al. (2020) and Jang et al. (2007) solve regime-switching with costs under *observed* regimes; Nystrup et al. (2018, 2019) do HMM-filtered MPC with costs empirically. I found no paper that solves the partially observed (filtered-belief) problem with proportional costs and then tests the resulting belief-dependent no-trade band on long historical data.

---

## 7. Filtering and learning under regimes

**Björk, T., Davis, M. H. A., & Landén, C. (2010). Optimal investment under partial information.** *Mathematical Methods of Operations Research* 71(2):371-399. DOI 10.1007/s00186-010-0301-x. [CR] `bjork2010optimal`

**Bäuerle, N., & Rieder, U. (2011). Markov Decision Processes with Applications to Finance.** Springer (Universitext). DOI 10.1007/978-3-642-18324-9. Chapter 5, "Partially observable Markov decision processes," DOI 10.1007/978-3-642-18324-9_5. [CR] `bauerle2011mdp`

**Rieder, U., & Bäuerle, N. (2005). Portfolio optimization with unobservable Markov-modulated drift process.** *Journal of Applied Probability* 42(2):362-378. DOI 10.1239/jap/1118777176. [CR] `rieder2005portfolio`

**Bäuerle, N., & Rieder, U. (2004). Portfolio optimization with Markov-modulated stock prices and interest rates.** *IEEE Transactions on Automatic Control* 49(3):442-447. DOI 10.1109/TAC.2004.824471. [CR] `bauerle2004markov`

**Sass, J., & Haussmann, U. G. (2004). Optimizing the terminal wealth under partial information: The drift process as a continuous time Markov chain.** *Finance and Stochastics* 8(4):553-577. DOI 10.1007/s00780-004-0132-9. [CR + WEB: IDEAS] `sass2004optimizing`
- Explicit optimal strategy in terms of the unnormalized (Wonham-type) filter; EM estimation; applied to historical prices.

**Honda, T. (2003). Optimal portfolio choice for unobservable and regime-switching mean returns.** *Journal of Economic Dynamics and Control* 28(1):45-78. DOI 10.1016/S0165-1889(02)00106-9. [CR] `honda2003optimal`
- Shows the optimal policy under filtering has a hedging component against belief changes; myopic plug-in of filtered means is suboptimal.

**Veronesi, P. (1999). Stock market overreaction to bad news in good times: A rational expectations equilibrium model.** *Review of Financial Studies* 12(5):975-1007. DOI 10.1093/rfs/12.5.975. [CR] `veronesi1999overreaction`
- Equilibrium with a hidden two-state drift and Bayesian learning: belief uncertainty itself drives volatility.

**Lakner, P. (1998). Optimal trading strategy for an investor: The case of partial information.** *Stochastic Processes and their Applications* 76(1):77-97. DOI 10.1016/S0304-4149(98)00032-5. [CR] `lakner1998optimal`

**Elliott, R. J., & van der Hoek, J. (1997). An application of hidden Markov models to asset allocation problems.** *Finance and Stochastics* 1(3):229-238. DOI 10.1007/s007800050022. [CR] `elliott1997hmm`

**Wonham, W. M. (1964). Some applications of stochastic differential equations to optimal nonlinear filtering.** *Journal of the Society for Industrial and Applied Mathematics, Series A: Control* 2(3):347-369. DOI 10.1137/0302028. [CR] `wonham1964filtering`

**Karatzas, I., & Zhao, X. (2001). Bayesian adaptive portfolio optimization.** In *Option Pricing, Interest Rates and Risk Management*, Cambridge University Press, pp. 632-669. DOI 10.1017/CBO9780511569708.018. [CR; Crossref has no year on the chapter, 2001 is the book's publication year and is UNVERIFIED, so this entry is left out of refs.bib]

---

## 8. POMDP and RL for portfolios

### POMDP foundations

**Krishnamurthy, V. (2016). Partially Observed Markov Decision Processes: From Filtering to Controlled Sensing.** Cambridge University Press. DOI 10.1017/CBO9781316471104. [CR] `krishnamurthy2016pomdp`

**Hauskrecht, M. (2000). Value-function approximations for partially observable Markov decision processes.** *Journal of Artificial Intelligence Research* 13:33-94. DOI 10.1613/jair.678. [CR] `hauskrecht2000value`
- Formal comparison of QMDP, fast informed bound and other approximations; shows QMDP is an upper bound that ignores the value of information. Useful for arguing that a "regime-probability-weighted MDP policy" is a QMDP-type approximation.

**Kaelbling, L. P., Littman, M. L., & Cassandra, A. R. (1998). Planning and acting in partially observable stochastic domains.** *Artificial Intelligence* 101(1-2):99-134. DOI 10.1016/S0004-3702(98)00023-X. [CR] `kaelbling1998planning`

**Littman, M. L., Cassandra, A. R., & Kaelbling, L. P. (1995). Learning policies for partially observable environments: Scaling up.** In *Machine Learning Proceedings 1995* (Proc. 12th ICML), pp. 362-370. Morgan Kaufmann. DOI 10.1016/B978-1-55860-377-6.50052-9. [CR] `littman1995learning`
- Introduces QMDP.

### RL for portfolios (credible sources only)

**Hambly, B., Xu, R., & Yang, H. (2023). Recent advances in reinforcement learning in finance.** *Mathematical Finance* 33(3):437-503. DOI 10.1111/mafi.12382. [CR] `hambly2023recent`

**Wang, H., & Zhou, X. Y. (2020). Continuous-time mean-variance portfolio selection: A reinforcement learning framework.** *Mathematical Finance* 30(4):1273-1308. DOI 10.1111/mafi.12281. [CR] `wang2020continuous`

**Kolm, P. N., & Ritter, G. (2019). Modern perspectives on reinforcement learning in finance.** SSRN, DOI 10.2139/ssrn.3449401. [CR for SSRN] `kolm2019modern`. Journal of Machine Learning in Finance placement: UNVERIFIED.

**Maggiolo, M., & Szehr, O. (2023). Overfitting in portfolio optimization.** *Journal of Risk Model Validation*. DOI 10.21314/JRMV.2023.005. [CR; volume/issue/pages UNVERIFIED, not in Crossref record] `maggiolo2023overfitting`
- Holdout (single train/test split) evaluation of neural-network portfolio models produces high OOS scores that do not survive proper evaluation; across ~30 models none consistently beats the short-sale-constrained minimum-variance rule (per abstract summary; the institutional summary is more favorable to NNs, so read the paper).

**Velay, M., Doan, B.-L., Rimmel, A., Popineau, F., & Daniel, F. (2023). Benchmarking robustness of deep reinforcement learning approaches to online portfolio management.** arXiv 2306.10950. [AX] `velay2023benchmarking`
- Most DRL algorithms tested were not robust; policies generalized poorly and degraded quickly in backtests.

**Lu, C. I. (2023). Evaluation of deep reinforcement learning algorithms for portfolio optimisation.** arXiv 2307.07694. [AX] `lu2023evaluation`
- On simulated data, sample complexity of standard DRL algorithms is too high for real-data use.

**Liu, X.-Y., Yang, H., Chen, Q., Zhang, R., Yang, L., Xiao, B., & Wang, C. D. (2020). FinRL: A deep reinforcement learning library for automated stock trading in quantitative finance.** arXiv 2011.09607. [AX] `liu2020finrl`

**Jiang, Z., Xu, D., & Liang, J. (2017). A deep reinforcement learning framework for the financial portfolio management problem.** arXiv 1706.10059. [AX] `jiang2017deep`

Not recommended as citations for claims (preprints with weak evaluation, listed only so you know they exist): Verma, Putri & Lesupi (2026), "Regime-based portfolio allocation using hidden Markov models and reinforcement learning," arXiv 2605.27848 [AX]; Oliveira, Sandfelder, Fujita, Dong & Cucuringu (2025), "Tactical asset allocation with macroeconomic regime detection," arXiv 2503.11499 [AX] (FRED-MD regimes, 2000-2022, 48-month windows; better than the first, and Cucuringu's group is credible, but still a preprint).

---

## 9. Private markets / allocator context

**Gourier, E., Phalippou, L., & Westerfield, M. M. (2024). Capital commitment.** *The Journal of Finance* 79(5):3407-3457. DOI 10.1111/jofi.13382. [CR] `gourier2024capital`
- Portfolio choice with uncertain capital calls; commitment risk as a cost of PE. The theory piece closest to an LP-level "denominator effect" model.

**Brown, G., Harris, R., Hu, W., Jenkinson, T., Kaplan, S. N., & Robinson, D. T. (2021). Can investors time their exposure to private equity?** *Journal of Financial Economics* 139(2):561-577. DOI 10.1016/j.jfineco.2020.08.014. [CR] `brown2021timing`

**Ang, A., Chen, B., Goetzmann, W. N., & Phalippou, L. (2018). Estimating private equity returns from limited partner cash flows.** *The Journal of Finance* 73(4):1751-1783. DOI 10.1111/jofi.12688. [CR] `ang2018estimating`

**Harris, R. S., Jenkinson, T., & Kaplan, S. N. (2014). Private equity performance: What do we know?** *The Journal of Finance* 69(5):1851-1882. DOI 10.1111/jofi.12154. [CR] `harris2014private`

**Phalippou, L., & Gottschalg, O. (2009). The performance of private equity funds.** *Review of Financial Studies* 22(4):1747-1776. DOI 10.1093/rfs/hhn014. (Crossref issued 2008 online.) [CR] `phalippou2009performance`

**Kaplan, S. N., & Schoar, A. (2005). Private equity performance: Returns, persistence, and capital flows.** *The Journal of Finance* 60(4):1791-1823. DOI 10.1111/j.1540-6261.2005.00780.x. [CR] `kaplan2005private`

**Takahashi, D., & Alexander, S. (2002). Illiquid alternative asset fund modeling.** *The Journal of Portfolio Management* 28(2):90-100. DOI 10.3905/jpm.2002.319836. [CR] `takahashi2002illiquid`
- The Yale model of PE contributions, distributions and NAV.

**Dimmock, S. G., Wang, N., & Yang, J. (2019). The endowment model and modern portfolio theory.** NBER WP 25559, DOI 10.3386/w25559. [CR for NBER WP] `dimmock2019endowment`. Journal publication (reportedly *Management Science*): UNVERIFIED.

**Granger, N., Harvey, C. R., Rattray, S., & Van Hemert, O. (2020). Strategic rebalancing.** *The Journal of Portfolio Management* 46(6):10-31. DOI 10.3905/jpm.2020.1.150. [CR] `granger2020strategic`
- Rebalancing a 60/40 is effectively short trend; adding trend or delayed rebalancing reduces drawdowns. Relevant to how a regime overlay interacts with policy rebalancing.

**Denominator effect.** I found no peer-reviewed paper with this as its subject. Sources are practitioner research (Eaton Vance / Morgan Stanley IM, "Deconstructing the denominator effect," on 2022 US pension PE allocations; NEPC, "Taking stock: denominator effect"; CFA Institute Enterprising Investor blog). UNVERIFIED as citable academic sources. In the paper, define the mechanism yourself (public-market drawdown + stale private NAVs push the private share above target, constraining new commitments and forcing rebalancing out of public risk) and cite Gourier-Phalippou-Westerfield (2024), Brown et al. (2021) and Takahashi-Alexander (2002) for the modeling pieces.

---

## Gaps

1. **No strict real-time, ~100-year evaluation of regime or jump-model allocation exists that I could find.** Searched Crossref, arXiv, and the open web for 2024-2026 work (SSRN itself returns 403 to automated fetches, so an SSRN-only working paper could have been missed). The longest jump-model OOS is 1990-2023, equity-only, 0/1 vs T-bills (Shu, Yu & Mulvey 2024, JAM). Multi-asset jump-model work starts OOS in 2007. Century-scale evidence exists only for simpler rules: trend (Hurst et al. 2017, from 1880; Lempérière et al. 2014), volatility targeting (Harvey et al. 2018, from as early as 1926), MA timing (Zakamulin 2017, from 1860). None of these use a fitted regime model, and none re-run the full model-design search in real time in the Pesaran-Timmermann (1995) sense.
2. **Design-choice leakage in the jump-model papers.** The jump penalty is tuned walk-forward, but feature families, halflives, number of states, window lengths, smoothing and dropped features were set with the whole sample visible. No PBO, deflated Sharpe, or SPA test is reported. A paper that freezes every design choice on pre-1950 data and evaluates 1950-2025 untouched would be new.
3. **No same-protocol horse race.** Jump models are benchmarked against HMMs and buy-and-hold. Nobody has compared JM vs 10-month SMA vs 12-month TSMOM vs capped vol targeting under one protocol, one cost model and one action space (0-100% equity, remainder bonds or bills).
4. **Belief-state decision rules are untested empirically.** Theory (Honda 2003; Rieder & Bäuerle 2005; Sass & Haussmann 2004; Bäuerle & Rieder 2011) gives optimal policies as functions of the filtered regime probability, including hedging of belief changes. Theory with costs and regimes exists only for observed regimes (Jang et al. 2007; Collin-Dufresne, Daniel & Sağlam 2020). Empirical papers use hard 0/1 labels or plug-in probabilities, which amounts to a QMDP-style approximation (Littman et al. 1995; Hauskrecht 2000). A belief-dependent no-trade band, estimated in real time and tested over a century, is unclaimed territory.
5. **Costs are thin.** 5-10 bps one-way on index total returns, with annual turnover from 2x up to 12x. No era-specific cost model (pre-1980 commissions, pre-futures index replication) in any regime paper.
6. **Real-time macro data.** Regime papers that use macro features (Kritzman et al. 2012 growth/inflation regimes; Shu et al. 2024 FRED features; Mulliner et al. 2025) do not, as far as the abstracts or text I read show, use vintage data from ALFRED or the Philadelphia Fed RTDSM. Price-only features avoid the issue, which is an argument for a price-only state in a 100-year study.
7. **Volatility-timing evidence and regime switching are evaluated separately.** The volatility-managed market portfolio is the one survivor of the critiques (Barroso & Detzel 2021). Whether a regime model adds anything beyond a capped vol-scaling rule (which removes the leverage channel Moreira-Muir rely on) has not been tested.
8. **LP-level context is mostly practitioner.** The denominator effect lacks a peer-reviewed empirical treatment. Linking a public-market regime signal to private-commitment pacing (Takahashi-Alexander cash-flow model + Gourier et al. commitment risk) is open.

## Items marked UNVERIFIED (do not cite as-is)

- Shu (2025) Princeton dissertation: exact title and metadata.
- Kinlaw, Kritzman, Metcalfe & Turkington (2023), JOIM: volume/issue/pages.
- Kolm & Ritter (2019): journal placement beyond SSRN.
- Maggiolo & Szehr (2023): volume/issue/pages.
- Dimmock, Wang & Yang: journal publication.
- Li et al. (2025): the claim that hyperparameters were chosen by max backtest Sharpe on the evaluation data.
- Aydınhan et al. (2024): empirical protocol details (data, penalty selection), and volume/pages (not yet assigned).
- All "denominator effect" practitioner sources.
- Fleming, Kirby & Ostdiek (2001): whether cash is in the asset set.

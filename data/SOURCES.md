# Raw data sources

All files under `data/raw/` were downloaded on **2026-10-08** with `curl` (no accounts, no API keys). SHA-256 values are of the files as saved on disk. Coverage and row counts come from `scripts/check_raw_data.py` (output pasted at the bottom). Rows count observations with at least one numeric value, so FRED rows exclude blank holiday entries.

Layout: `fred/`, `french/` (unzipped CSVs, original zips in `french/zips/`), `goyal/`, `philfed_rtdsm/`, `shiller/`, `jst/`, `aqr/`, `treasury/` (Fed GSW curve and Damodaran annual returns), `schwert/` (pre-CRSP daily/monthly stock returns).

## Notes by source

### 1. Goyal-Welch / Goyal-Welch-Zafirov
- Page: https://sites.google.com/view/agoyal145 . Data sits on Google Drive behind public share links; no login.
- `GW2008_PredictorData_updated_2025.xlsx` is the classic PredictorData file ("Updated data (up to 2025)"). Columns: yyyymm, Index, D12, E12, b/m, tbl, AAA, BAA, lty, ntis, Rfree, infl, ltr, corpr, svar, csp, CRSP_SPvw, CRSP_SPvwx. Monthly 1871-01..2025-12. Per-column starts: CRSP_SPvw/ltr/corpr 1926-01, svar 1885-02, ntis 1926-12, b/m 1921-03, tbl 1920-01, infl 1913-02; csp only 1937-05..2002-12.
- Goyal's page states that from 2022 on, lty comes from FRED and ltr/corpr from Bloomberg indices. Expect a splice at 2022-01 in the bond-return series.
- `GWZ2024_GW2008_alldata_2025.xlsx` merges GW (2008) and GWZ (2024) predictors into one file (full-sample versions only) with a ReadMe sheet. Column names differ from the GW file (`price`, `ret`, `retx`, `d/p`, `tms`, `dfy`, ...).
- `GWZ2024_data_2025_csv.zip` (27 MB zipped, 360 MB unzipped, kept zipped) holds the 46 real-time predictor matrices from the RFS 2024 paper. Google Drive serves a "too large to virus-scan" interstitial; the URL with `confirm=t` skips it.

### 2. Kenneth French Data Library
- Index: https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html . Files built from the **202608 CRSP** database (data through 2026-08-31).
- Values are percent. Monthly files also contain annual blocks below the monthly table; 10_Industry has 8 blocks (VW/EW monthly, VW/EW annual, number of firms, avg size, ...). Parse only the first block unless you need the others.
- RF source change: Ibbotson 1-month T-bill through 2024-05, ICE BofA US 1-Month Treasury Bill Index from 2024-06 (stated in the file header).
- International/developed files are built from **Bloomberg** data and start 1990-07 (Mom 1990-11, Emerging 1989-07). They cannot extend the regime study before 1990.
- Daily momentum starts 1926-11-03; daily Mkt/SMB/HML/RF start 1926-07-01.

### 3. FRED
- URL template `https://fred.stlouisfed.org/graph/fredgraph.csv?id=SERIES`. Header is `observation_date,SERIES`; missing values are empty cells. Note: curl over HTTP/2 failed with stream errors, `--http1.1` worked.
- **Truncated / discontinued:**
  - `BAMLH0A0HYM2`, `BAMLC0A0CM`: only 2023-10-09 onward. FRED now publishes just a rolling 3-year window of ICE BofA series under ICE's license. Full history needs another source.
  - `VXOCLS`: discontinued by CBOE, ends 2021-09-23.
  - `TEDRATE`: discontinued with LIBOR, ends 2022-01-21.
  - `UMCSENT`: quarterly before 1978 (210 blank months).
  - `DTWEXBGS` starts only 2006-01.
- Short histories relative to 1926: VIXCLS 1990, NFCI/ANFCI 1971, STLFSI4 1993-12, DBAA 1986, DAAA 1983, T10Y3M 1982, DGS2/T10Y2Y 1976-06. Long ones: USREC/USRECM 1854-12, BAA/AAA/INDPRO 1919, PAYEMS 1939, TB3MS 1934.
- FRED marks some series as copyrighted by the originator (Moody's for AAA/BAA/DAAA/DBAA, ICE for BAML, University of Michigan for UMCSENT). Fine for research; check before redistributing.

### 4. Philadelphia Fed RTDSM
- Variable pages: https://www.philadelphiafed.org/surveys-and-data/real-time-data-research/{ipt,employ,ruc,cpi,routput}.
- Monthly vintages exist for IPT (`iptMvMd`, vintages 1962M11..2026M9), EMPLOY (`employMvMd`, 1964M12..2026M9) and real GDP (`routputMvQd`, 1965M11..2026M10).
- **RUC and CPI only have quarterly vintages** (`rucQvMd`, `cpiQvMd`, vintages 1965Q4..2026Q3). The guessed `rucMvMd.xlsx`/`cpiMvMd.xlsx` URLs return an HTML error page. ALFRED has monthly vintages for both, but bulk access goes through its API, which needs a key, so it was skipped.
- Missing values are the string `#N/A`. Some workbooks have malformed document properties that make plain `openpyxl` crash; the check script patches around it.
- Also saved the first/second/third release tables for IPT, EMPLOY and ROUTPUT.

### 5. Shiller
- The Yale URL (`http://www.econ.yale.edu/~shiller/data/ie_data.xls`) still serves a file, but it was last saved 2023-09 and ends 2023-09. Kept as `ie_data_yale_stale.xls` for reference only.
- The maintained file is linked from https://shillerdata.com/ (hosted on img1.wsimg.com). It runs 1871-01..2026-10. The 2026-10 row is partial (October price is a month-to-date average, CPI is extrapolated).
- Date column is a float `yyyy.mm`, so October appears as `yyyy.1`. Parse as `round((x - int(x)) * 100)`.
- `.xls` needs `xlrd` (not installed in the base conda env; the check ran in a scratch venv with xlrd 2.0.2).

### 6. Jordà-Schularick-Taylor Macrohistory
- Page: https://www.macrohistory.net/database/ . Latest release is **R6**, covering 18 countries, 1870-2020. No newer release exists, so this source ends in **2020**.
- License: **CC BY-NC-SA 4.0**; commercial data vendors may not redistribute. Must cite Jordà, Schularick and Taylor (and Jordà et al. 2019 "The Rate of Return on Everything" for the return series).

### 7. AQR
- Index: https://www.aqr.com/Insights/Datasets . Direct `.xlsx` downloads; no login (the "Log In" link on the page is for MyAQR and is not needed).
- Downloaded: TSMOM factors (1985-01..2026-05), Century of Factor Premia (1926-07..2026-02), BAB monthly/daily, QMJ monthly/daily, Value and Momentum Everywhere factors (1972-01..2026-07), Credit Risk Premium paper data (1926-01..2014-12; corporate and Treasury excess returns), Commodities for the Long Run (1877-02..2025-05).
- BAB and QMJ workbooks also carry AQR's own MKT, SMB, HML FF, HML Devil, UMD and RF sheets by country (US MKT daily from 1926-07-01).
- No volatility-managed portfolio dataset is published on AQR's dataset page. (Moreira-Muir volatility-managed data live on the authors' own pages; not downloaded.)
- Update lags differ by file: TSMOM ends 2026-05, Century ends 2026-02, Commodities ends 2025-05, Credit Risk Premium frozen at 2014-12.
- Dates come in mixed formats (`MM/DD/YYYY` strings, real datetimes, and ISO strings for pre-1900 rows).

### 8. Long Treasury total returns
- Goyal `ltr` (long-term government bond total return) covers 1926-01..2025-12 monthly and is the primary series. From 2022 it is a Bloomberg index (splice).
- H.15 is yields only; the yields are already covered via FRED (GS10, DGS10, TB3MS, DTB3, GS1, DGS2).
- Added `treasury/feds200628.csv`: Gürkaynak-Sack-Wright fitted Treasury curve, daily from 1961-06-14 (10y zero from 1971-08-16, 30y from 1985-11-25). Usable to build constant-maturity zero-coupon bond returns. Not an official Fed statistical release (staff research product). First 9 lines are notes; data header is on line 10.
- Added `treasury/histretSP.xls`: Damodaran annual returns 1928-2025 on S&P 500, 3m T-bill, 10y T-bond, Baa corporates, real estate, gold. Annual only; useful as a cross-check.
- AQR Credit Risk Premium file adds monthly Treasury excess returns (GOVT_XS) for 1926-2014.

### 9. Realized volatility before 1990
- Confirmed: French daily factors start 1926-07-01, so daily Mkt (= Mkt-RF + RF) gives realized volatility from July 1926. AQR's daily US MKT sheet also starts 1926-07-01.
- Goyal `svar` (monthly sum of squared daily returns) runs from 1885-02.
- Added Schwert's daily returns (`schwert/STKDATD.DAT`, Dow Jones composite 1885-02-16..1928-01-03, S&P composite 1928-01-04..1962-07-02, 22,474 days) and monthly returns 1802-1925 (`STKDATM.DAT`). Source page: https://www.billschwert.com/dstock.htm . **License: academic use with citation to Schwert (1990, Journal of Business); the author asks that the files not be passed on to others and not be used commercially without permission.** Keep them out of any public repo.
- VIX starts 1990 and VXO 1986, so implied-vol regimes before 1986 need a realized-vol proxy.

## Skipped / failed
- Nothing required a login or key. No source was skipped for that reason.
- Not obtainable for free: full-history ICE BofA OAS (FRED truncates to 3 years); monthly-vintage RUC and CPI from RTDSM (Philly Fed publishes quarterly vintages only).
- Not attempted: ALFRED bulk vintages (API needs a key).

## Per-file manifest

| file | source URL | SHA-256 | coverage (first..last) | rows | frequency | units |
|---|---|---|---|---|---|---|
| `aqr/Betting-Against-Beta-Equity-Factors-Daily.xlsx` | https://www.aqr.com/-/media/AQR/Documents/Insights/Data-Sets/Betting-Against-Beta-Equity-Factors-Daily.xlsx | `c34f1ac4130f69dd73440dd62a53caf22df47bc7cc50f5cf544f8e522c28a8c6` | 1930-12-01..2026-07-31 | 25369 | daily | decimal returns (excess returns for factors) |
| `aqr/Betting-Against-Beta-Equity-Factors-Monthly.xlsx` | https://www.aqr.com/-/media/AQR/Documents/Insights/Data-Sets/Betting-Against-Beta-Equity-Factors-Monthly.xlsx | `b98d9ce68033e9ac38812737ab7444e6883348bcae6e4573abcdaa94fd164514` | 1930-12-31..2026-07-31 | 1148 | monthly | decimal returns (excess returns for factors) |
| `aqr/Century-of-Factor-Premia-Monthly.xlsx` | https://www.aqr.com/-/media/AQR/Documents/Insights/Data-Sets/Century-of-Factor-Premia-Monthly.xlsx | `0bf8ba978e64964282ead98a6a25691218d4517d07c98c89e2716706f6f0a127` | 1926-07-30..2026-02-27 | 1196 | monthly | decimal returns (excess returns for factors) |
| `aqr/Commodities-for-the-Long-Run-Index-Level-Data-Monthly.xlsx` | https://www.aqr.com/-/media/AQR/Documents/Insights/Data-Sets/Commodities-for-the-Long-Run-Index-Level-Data-Monthly.xlsx | `eeb89c65fa7dca2bfbbebb7af2cbecade7b470d6a4da52883e9413a162b5fe75` | 1877-02-28..2025-05-30 | 1780 | monthly | decimal returns (excess returns for factors) |
| `aqr/Credit-Risk-Premium-Preliminary-Paper-Data.xlsx` | https://www.aqr.com/-/media/AQR/Documents/Insights/Data-Sets/Credit-Risk-Premium-Preliminary-Paper-Data.xlsx | `9653fa3315feb92b7d4bbe276c049543d8b97dabea9c54b6cd9a499c95d93f2d` | 1926-01-29..2014-12-31 | 1068 | monthly | decimal returns (excess returns for factors) |
| `aqr/Quality-Minus-Junk-Factors-Daily.xlsx` | https://www.aqr.com/-/media/AQR/Documents/Insights/Data-Sets/Quality-Minus-Junk-Factors-Daily.xlsx | `6e0d68577fcd87e182c51902cd35d4dd7252d211d0f62327a87a1c7d9456de7e` | 1957-07-01..2026-07-31 | 17769 | daily | decimal returns (excess returns for factors) |
| `aqr/Quality-Minus-Junk-Factors-Monthly.xlsx` | https://www.aqr.com/-/media/AQR/Documents/Insights/Data-Sets/Quality-Minus-Junk-Factors-Monthly.xlsx | `b5453aec115f37fa79caa1b8e3fb7dca9c6ebc9d486e4c10aaf4270d9790a8f6` | 1957-07-31..2026-07-31 | 829 | monthly | decimal returns (excess returns for factors) |
| `aqr/Time-Series-Momentum-Factors-Monthly.xlsx` | https://www.aqr.com/-/media/AQR/Documents/Insights/Data-Sets/Time-Series-Momentum-Factors-Monthly.xlsx | `33470930e2269c0d97be4732ec2d9c27ddbc69ac8133b059a263e27400263eeb` | 1985-01-31..2026-05-29 | 497 | monthly | decimal returns (excess returns for factors) |
| `aqr/Value-and-Momentum-Everywhere-Factors-Monthly.xlsx` | https://www.aqr.com/-/media/AQR/Documents/Insights/Data-Sets/Value-and-Momentum-Everywhere-Factors-Monthly.xlsx | `ed9ddbdee42affe481035b88af6d0c32365bc6aa3dc0c780806e066ba4f4386e` | 1972-01-31..2026-07-31 | 655 | monthly | decimal returns (excess returns for factors) |
| `fred/AAA.csv` | https://fred.stlouisfed.org/graph/fredgraph.csv?id=AAA | `15248259177710745867656c413bb2bae549c6485ca3acb7eed348a812f497ac` | 1919-01-01..2026-09-01 | 1293 | monthly | % (Moody's Aaa seasoned corp yield, monthly avg) |
| `fred/ANFCI.csv` | https://fred.stlouisfed.org/graph/fredgraph.csv?id=ANFCI | `271421c357bf56178191bd2ab6fb0a53589772880b9b091f620b991ec12f393c` | 1971-01-08..2026-10-02 | 2909 | weekly (Fri) | index, adjusted NFCI |
| `fred/BAA.csv` | https://fred.stlouisfed.org/graph/fredgraph.csv?id=BAA | `3396297d0b2f8f4e8bb467207286c33c04d97bfe37b25bc5a97da6bafc615e93` | 1919-01-01..2026-09-01 | 1293 | monthly | % (Moody's Baa seasoned corp yield, monthly avg) |
| `fred/BAMLC0A0CM.csv` | https://fred.stlouisfed.org/graph/fredgraph.csv?id=BAMLC0A0CM | `754a2a2844983c0b1bc24e15ffa19d82b846ea4f2a4beda42d5741f830b0e706` | 2023-10-09..2026-10-06 | 784 | daily | % OAS |
| `fred/BAMLH0A0HYM2.csv` | https://fred.stlouisfed.org/graph/fredgraph.csv?id=BAMLH0A0HYM2 | `bdcc75849281bd918233ff1d076ad4725722b2ef5d51f7ff04bad8ffb81942f6` | 2023-10-09..2026-10-06 | 785 | daily | % OAS |
| `fred/CPIAUCSL.csv` | https://fred.stlouisfed.org/graph/fredgraph.csv?id=CPIAUCSL | `f8ecddf53a9a9a74dda92c2c4204e6039466fcb744bc74171b73b5f6aac48119` | 1947-01-01..2026-08-01 | 955 | monthly | index 1982-84=100, SA |
| `fred/DAAA.csv` | https://fred.stlouisfed.org/graph/fredgraph.csv?id=DAAA | `5a2b9dd5a61282aa628c4e4a334a0d702863c31e3a9c473ff4fb433958c1da12` | 1983-01-03..2026-10-06 | 10986 | daily | % |
| `fred/DBAA.csv` | https://fred.stlouisfed.org/graph/fredgraph.csv?id=DBAA | `6a44fe424580c86fd61d81f618485dd0be186eaa854a78ed64b43517406e30fc` | 1986-01-02..2026-10-06 | 10227 | daily | % |
| `fred/DCOILWTICO.csv` | https://fred.stlouisfed.org/graph/fredgraph.csv?id=DCOILWTICO | `0440ec6862dccc8c753a91d63d287808e086e4b4f1267515b9e90209f3f2e061` | 1986-01-02..2026-10-06 | 9517 | daily | USD per barrel |
| `fred/DGS10.csv` | https://fred.stlouisfed.org/graph/fredgraph.csv?id=DGS10 | `422b1048a3b3eebec2e9cdd0847893112e96f266b85b29314df950a85b942232` | 1962-01-02..2026-10-06 | 16176 | daily | % (10y CMT) |
| `fred/DGS2.csv` | https://fred.stlouisfed.org/graph/fredgraph.csv?id=DGS2 | `18245f9fc7b57d908f5181970d1243f720d374f1bd294f1e6920bc84a6b5e3a5` | 1976-06-01..2026-10-06 | 12584 | daily | % (2y CMT) |
| `fred/DTB3.csv` | https://fred.stlouisfed.org/graph/fredgraph.csv?id=DTB3 | `cccb39e8bb4caf421ffef5335510d72ee7b46de034ec98b381fb0a2117a27007` | 1954-01-04..2026-10-06 | 18182 | daily | % (3m T-bill, discount basis) |
| `fred/DTWEXBGS.csv` | https://fred.stlouisfed.org/graph/fredgraph.csv?id=DTWEXBGS | `75edd28ba1eceade938fa6621edfebc4d4e9cbcc846c6f07be27f8aef0ead321` | 2006-01-02..2026-10-02 | 5203 | daily | index Jan 2006=100 |
| `fred/FEDFUNDS.csv` | https://fred.stlouisfed.org/graph/fredgraph.csv?id=FEDFUNDS | `74680b2d09bb28f90fb30c1c09e93ac2d443de1b7345ba5a9112b3eca9be0a25` | 1954-07-01..2026-09-01 | 867 | monthly | %, monthly avg of effective rate |
| `fred/GS1.csv` | https://fred.stlouisfed.org/graph/fredgraph.csv?id=GS1 | `c462ef0a7d8fbfaeef71405eaacbe59a1ea175ded09a149cf4e8e0760d9c62cd` | 1953-04-01..2026-09-01 | 882 | monthly | % (1y CMT, monthly avg) |
| `fred/GS10.csv` | https://fred.stlouisfed.org/graph/fredgraph.csv?id=GS10 | `40323f225e613a19a4eec7eef20523dec10764de21c70cd1416a7379fb7f13b6` | 1953-04-01..2026-09-01 | 882 | monthly | % (10y CMT, monthly avg) |
| `fred/ICSA.csv` | https://fred.stlouisfed.org/graph/fredgraph.csv?id=ICSA | `0910abb3f9bab87d1a277f3c567ea7c3d83cc2260f5a4a9587eebe306fb80823` | 1967-01-07..2026-09-26 | 3117 | weekly (Sat) | number of claims, SA |
| `fred/INDPRO.csv` | https://fred.stlouisfed.org/graph/fredgraph.csv?id=INDPRO | `1a916926060d09b970880153da76d36040505666dbe686ae2abda1ff7eba6279` | 1919-01-01..2026-08-01 | 1292 | monthly | index 2017=100, SA |
| `fred/M2SL.csv` | https://fred.stlouisfed.org/graph/fredgraph.csv?id=M2SL | `63b673baffae16f7683963ddde0664012a7ac93ab775a82d3c98a0311e103e5a` | 1959-01-01..2026-08-01 | 812 | monthly | billions USD, SA |
| `fred/NFCI.csv` | https://fred.stlouisfed.org/graph/fredgraph.csv?id=NFCI | `e7f217a41c0530b43033cd4d7ebf9c76bf455e9ed92e71110d6bfad80b5b0ed7` | 1971-01-08..2026-10-02 | 2909 | weekly (Fri) | index, 0 = average conditions, +ve = tighter |
| `fred/PAYEMS.csv` | https://fred.stlouisfed.org/graph/fredgraph.csv?id=PAYEMS | `c8c429818ed73de6db985f4ff565d64bd2a5ba66a6b651b39373a1532924fc0e` | 1939-01-01..2026-09-01 | 1053 | monthly | thousands of persons, SA |
| `fred/STLFSI4.csv` | https://fred.stlouisfed.org/graph/fredgraph.csv?id=STLFSI4 | `09959dd9b9acbc87de0d45e16c8ef743c8c68cdeb63e569dade015d5fca8c37e` | 1993-12-31..2026-10-02 | 1710 | weekly (Fri) | index, 0 = normal stress |
| `fred/T10Y2Y.csv` | https://fred.stlouisfed.org/graph/fredgraph.csv?id=T10Y2Y | `cdac50d4be424408a3ba01849706a7b6610c93af9ab6fd1f1baeaa44a8ed9b19` | 1976-06-01..2026-10-07 | 12585 | daily | percentage points |
| `fred/T10Y3M.csv` | https://fred.stlouisfed.org/graph/fredgraph.csv?id=T10Y3M | `00a617ba5ec4b59f5dc965e540bbd539328b43c78a80b2cdc06b4ff7e077f8b0` | 1982-01-04..2026-10-07 | 11194 | daily | percentage points |
| `fred/TB3MS.csv` | https://fred.stlouisfed.org/graph/fredgraph.csv?id=TB3MS | `631bc444a8c5370c3a2df12f484a67ae7b9a68c00fe8a33215895fb49c8cc08c` | 1934-01-01..2026-09-01 | 1113 | monthly | % (3m T-bill secondary mkt, discount basis) |
| `fred/TEDRATE.csv` | https://fred.stlouisfed.org/graph/fredgraph.csv?id=TEDRATE | `291d6007c287e3a1a56fff7879dcfa5aaa44620bc0a68cb2ab8ccf032795c99d` | 1986-01-02..2022-01-21 | 8853 | daily | % |
| `fred/UMCSENT.csv` | https://fred.stlouisfed.org/graph/fredgraph.csv?id=UMCSENT | `27ce18aeda2ab875e799cf856913f95330bb6013fe75d8358c63a6f0c02a8e95` | 1952-11-01..2026-08-01 | 676 | monthly (quarterly pre-1978) | index 1966:Q1=100 |
| `fred/UNRATE.csv` | https://fred.stlouisfed.org/graph/fredgraph.csv?id=UNRATE | `621ff6fadf50910cb7a21ee20ba610c247cb043b29b4e05c4c1a72fadca2a06c` | 1948-01-01..2026-09-01 | 944 | monthly | %, SA |
| `fred/USREC.csv` | https://fred.stlouisfed.org/graph/fredgraph.csv?id=USREC | `a42a3581fe9c260dd3627febc84a7d563e5ed162cc7085a7518ebde99dc3c3b4` | 1854-12-01..2026-09-01 | 2062 | monthly | 0/1 NBER, period after peak through trough |
| `fred/USRECM.csv` | https://fred.stlouisfed.org/graph/fredgraph.csv?id=USRECM | `7f4b4ab907b2699b47db00f26c3009d9d16014f0b0848d7d43e04f8c6e5a0a02` | 1854-12-01..2026-09-01 | 2062 | monthly | 0/1 NBER, peak through trough |
| `fred/VIXCLS.csv` | https://fred.stlouisfed.org/graph/fredgraph.csv?id=VIXCLS | `2f5c1214537be30fbf01e26d0a0b4ec79624ba5858e0c8bc6c9da31eb8f5d5b4` | 1990-01-02..2026-10-06 | 9289 | daily | index points (CBOE VIX close) |
| `fred/VXOCLS.csv` | https://fred.stlouisfed.org/graph/fredgraph.csv?id=VXOCLS | `3ab3e522630a6b404fda6cd2d7ef33834139218bf00f5a290aa089361dd334e8` | 1986-01-02..2021-09-23 | 9002 | daily | index points (CBOE VXO close) |
| `french/10_Industry_Portfolios.csv` | https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/10_Industry_Portfolios_CSV.zip (unzipped) | `18ed376fc42e2327ceaf3d65a02521a6512e7f9e3001007c4da69d7db108aa82` | 192607..202608 | 1202 | monthly + annual | % per period (returns); -99.99/-999 = missing |
| `french/Asia_Pacific_ex_Japan_3_Factors.csv` | https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/Asia_Pacific_ex_Japan_3_Factors_CSV.zip (unzipped) | `39a6769fce267563fde60337f3ac03bc9774d9669d4a15147f67ecb4fea1e611` | 199007..202608 | 434 | monthly + annual | % per period (returns); -99.99/-999 = missing |
| `french/Developed_3_Factors.csv` | https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/Developed_3_Factors_CSV.zip (unzipped) | `1d2658c5d3945a270c7dbf3465687ad8432cd611844e74d0869cba2cfb010419` | 199007..202608 | 434 | monthly + annual | % per period (returns); -99.99/-999 = missing |
| `french/Developed_3_Factors_Daily.csv` | https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/Developed_3_Factors_Daily_CSV.zip (unzipped) | `5b52e9e710376ac5dc7da6d7684e33e883bf6167b38cd451254e43e2fb6cf812` | 19900702..20260831 | 9436 | daily | % per period (returns); -99.99/-999 = missing |
| `french/Developed_MOM_Factor.csv` | https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/Developed_Mom_Factor_CSV.zip (unzipped) | `b80cecb982d919157e7a30ad3a7e3c4fcec13efed5194967185530aa0155c344` | 199011..202608 | 430 | monthly + annual | % per period (returns); -99.99/-999 = missing |
| `french/Developed_ex_US_3_Factors.csv` | https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/Developed_ex_US_3_Factors_CSV.zip (unzipped) | `68fd8d00a0a59704dd24d3fa6ec2eebc66ea1b1bf21a96270b2f1476bcb6010c` | 199007..202608 | 434 | monthly + annual | % per period (returns); -99.99/-999 = missing |
| `french/Developed_ex_US_3_Factors_Daily.csv` | https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/Developed_ex_US_3_Factors_Daily_CSV.zip (unzipped) | `6287bbbcba03be35c8dbe99d21364967f07eb087893079167f41ec8a9047f185` | 19900702..20260831 | 9436 | daily | % per period (returns); -99.99/-999 = missing |
| `french/Developed_ex_US_MOM_Factor.csv` | https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/Developed_ex_US_Mom_Factor_CSV.zip (unzipped) | `5db255adb7d237972edb46125e7c8a3b196077cf8aabcc669c032c5effc5d461` | 199011..202608 | 430 | monthly + annual | % per period (returns); -99.99/-999 = missing |
| `french/Emerging_5_Factors.csv` | https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/Emerging_5_Factors_CSV.zip (unzipped) | `d960694ac438a0b3c95ee5c68245115930092df4ecfd9a6f9a75a01e9bbbefcc` | 198907..202608 | 446 | monthly + annual | % per period (returns); -99.99/-999 = missing |
| `french/Europe_3_Factors.csv` | https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/Europe_3_Factors_CSV.zip (unzipped) | `02b6024adf35e2e55aa5667944ff060fc09e734dfa869efaac00d3a7df8d47fd` | 199007..202608 | 434 | monthly + annual | % per period (returns); -99.99/-999 = missing |
| `french/F-F_Momentum_Factor.csv` | https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Momentum_Factor_CSV.zip (unzipped) | `613b628c5ffa8b957e03ad3a4ccd891d3aa6daafc1801dffb7db7376f2017bdc` | 192701..202608 | 1196 | monthly + annual | % per period (returns); -99.99/-999 = missing |
| `french/F-F_Momentum_Factor_daily.csv` | https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Momentum_Factor_daily_CSV.zip (unzipped) | `d4b3e98cb5afb1533af0d4568aa816de2aadac5bbff9a590c1c65e3392d7b05b` | 19261103..20260831 | 26216 | daily | % per period (returns); -99.99/-999 = missing |
| `french/F-F_Research_Data_Factors.csv` | https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_Factors_CSV.zip (unzipped) | `d7d7fe37b150b5b15c9c069b3ba101dfe1af568c6d7b5db6e73cd0a6c0c9e5e5` | 192607..202608 | 1202 | monthly + annual | % per period (returns); -99.99/-999 = missing |
| `french/F-F_Research_Data_Factors_daily.csv` | https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_Factors_daily_CSV.zip (unzipped) | `c2dc30c9e89eeea05a689c81fb426f4d76711270733b3731997615cbdff5b247` | 19260701..20260831 | 26317 | daily | % per period (returns); -99.99/-999 = missing |
| `french/Japan_3_Factors.csv` | https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/Japan_3_Factors_CSV.zip (unzipped) | `31d574c33677e8fb8749befe863ebafa7fb9f7221d1ac30c7259b34ddc8416e8` | 199007..202608 | 434 | monthly + annual | % per period (returns); -99.99/-999 = missing |
| `french/North_America_3_Factors.csv` | https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/North_America_3_Factors_CSV.zip (unzipped) | `d46863e8faf8f0a3069b74fcea64f93befee8b1e1d18b72136fb5c63ff3203dc` | 199007..202608 | 434 | monthly + annual | % per period (returns); -99.99/-999 = missing |
| `french/zips/10_Industry_Portfolios_CSV.zip` | https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/10_Industry_Portfolios_CSV.zip | `ebd937a4b995d821867aeb956a96f09a666386f38fa82516b7d1767ee4a49ae5` | - | - | - | original zip |
| `french/zips/Asia_Pacific_ex_Japan_3_Factors_CSV.zip` | https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/Asia_Pacific_ex_Japan_3_Factors_CSV.zip | `c0d835fa5db6092ab35714dfd8ca820b00b08cdf7bef1d151f33c725f4c67893` | - | - | - | original zip |
| `french/zips/Developed_3_Factors_CSV.zip` | https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/Developed_3_Factors_CSV.zip | `b6bdca31293c96af8117690707a9346d1174c5cd3f8ab662db6b616c46b73dfc` | - | - | - | original zip |
| `french/zips/Developed_3_Factors_Daily_CSV.zip` | https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/Developed_3_Factors_Daily_CSV.zip | `75b502cba8b0a7cc5752f67a6b6e2b217c66c5031453746ef8fb83516755f9a8` | - | - | - | original zip |
| `french/zips/Developed_Mom_Factor_CSV.zip` | https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/Developed_Mom_Factor_CSV.zip | `f2217d81ca76d749d1ee84dd8de80ec70db341c583b7c94a1960e3b807fa7931` | - | - | - | original zip |
| `french/zips/Developed_ex_US_3_Factors_CSV.zip` | https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/Developed_ex_US_3_Factors_CSV.zip | `83eda24f53a17c1612af370a9d48e53557dd9de029622b22ff350139d15731d5` | - | - | - | original zip |
| `french/zips/Developed_ex_US_3_Factors_Daily_CSV.zip` | https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/Developed_ex_US_3_Factors_Daily_CSV.zip | `f1a4eac34fa560cb559c0f14c8ea590227ad6ddaf806110d5c38cf169a1e406f` | - | - | - | original zip |
| `french/zips/Developed_ex_US_Mom_Factor_CSV.zip` | https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/Developed_ex_US_Mom_Factor_CSV.zip | `0b0941b3e504f4cc145e96deb066fb4bba9ae1b462f9270f37a14af63c4e63b3` | - | - | - | original zip |
| `french/zips/Emerging_5_Factors_CSV.zip` | https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/Emerging_5_Factors_CSV.zip | `303b5afb42232683f48f80178206a5cb99b1b755e4dc0493f9ec9b26dd74d103` | - | - | - | original zip |
| `french/zips/Europe_3_Factors_CSV.zip` | https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/Europe_3_Factors_CSV.zip | `529b7f1909b91343d02ad48b51f09dd137d38dd542f74d8c577c3872c2b6585a` | - | - | - | original zip |
| `french/zips/F-F_Momentum_Factor_CSV.zip` | https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Momentum_Factor_CSV.zip | `c06d1c2e9a5e4f6985879722f23c6bb585f46b34eaf3fcb681d4de887e353f3e` | - | - | - | original zip |
| `french/zips/F-F_Momentum_Factor_daily_CSV.zip` | https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Momentum_Factor_daily_CSV.zip | `ecf82b116e6ec56d2b79a2f27bd1d1598c217b5c6c25caa55b945bdd8a2c0b78` | - | - | - | original zip |
| `french/zips/F-F_Research_Data_Factors_CSV.zip` | https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_Factors_CSV.zip | `593f4fbef03181bc0b22ff6292f217689dd1fb79355049ca905d95b262040a66` | - | - | - | original zip |
| `french/zips/F-F_Research_Data_Factors_daily_CSV.zip` | https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_Factors_daily_CSV.zip | `2f29e22546069914890a712680a6f81f3680ebc3543b52864484d209ca13a7db` | - | - | - | original zip |
| `french/zips/Japan_3_Factors_CSV.zip` | https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/Japan_3_Factors_CSV.zip | `e116a250dff2e152d2c43359a99d1e478d7d3d94f35d3afb412af3a094f5db20` | - | - | - | original zip |
| `french/zips/North_America_3_Factors_CSV.zip` | https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/North_America_3_Factors_CSV.zip | `8dd66a61dea226dae28ec1092e869921a60df09d0c34d9d34a471bc089a5e64b` | - | - | - | original zip |
| `goyal/GW2008_PredictorData_updated_2025.xlsx` | https://drive.google.com/uc?export=download&id=1qwpl2R_DNujpU5YUkk8lacP1tTeMb9iJ | `8d210b779442a5a9206702060aac67c1de4283186c0f167ebdb4488d149be872` | 187101..202512 | 1860 | monthly/quarterly/annual sheets | levels in USD (Index, D12, E12); rates and returns in decimals |
| `goyal/GWZ2024_GW2008_alldata_2025.xlsx` | https://drive.google.com/uc?export=download&id=17mw_IpaiLFDrGnrPRQ2o1ugV5nJsZuD1 | `be74347c37d387fcdeeaf1f24a1332a6382f47943dd331906a5f9de0a30fe480` | 187101..202512 | 1860 | monthly/quarterly/annual sheets + ReadMe | decimals; see ReadMe sheet |
| `goyal/GWZ2024_data_2025_csv.zip` | https://drive.usercontent.google.com/download?id=1hBmVsCIzhVyzmt0FFno2oT-9aEcRVj1g&export=download&confirm=t | `43c0ab21c4ecd175aa13d1d69038d082d3b681df1b631a33d8c1076008a6022f` | 1926..2025 | 100 | M/Q/A/S per file suffix | 46 real-time predictor matrices (obs date x vintage) |
| `jst/JST_RORE_Documentation_R6.pdf` | https://www.macrohistory.net/app/download/9918957869/JST_RORE_Documentation_R6.pdf?t=1658254098 | `5fa4ec8e4986f6359ea27811bbb9772fa46a4fc644e081025276a720644908d0` | - | - | - | documentation (rate-of-return series) |
| `jst/JST_documentationR6.pdf` | https://www.macrohistory.net/app/download/9834516169/JST_documentationR6.pdf?t=1676279836 | `36b428724246409f52b760d7803bc05a1281677abc7a67d28567a21c1c44e1f2` | - | - | - | documentation |
| `jst/JSTdatasetR6.dta` | https://www.macrohistory.net/app/download/9834512469/JSTdatasetR6.dta?t=1763503850 | `b0ebb74a8d1b5b1bc9033fc46a6dcc578736afff8ce1e1086b7840f2649e79b3` | 1870..2020 | 2718 | annual | Stata 118, same content |
| `jst/JSTdatasetR6.xlsx` | https://www.macrohistory.net/app/download/9834512569/JSTdatasetR6.xlsx?t=1763503850 | `c1bb91fe56ea50d4f27af5c0fc897d481e89ae38ce41eaecab62134c9354981d` | 1870..2020 | 2718 | annual | country-year panel; returns decimal nominal local currency |
| `philfed_rtdsm/ROUTPUTQvQd.xlsx` | https://www.philadelphiafed.org/-/media/FRBP/Assets/Surveys-And-Data/real-time-data/data-files/xlsx/ROUTPUTQvQd.xlsx | `25433da00f46764a167590efe5c3e1c20a3e91e98ba0f49e6f92f058bc42c9e3` | 1947:Q1..2026:Q2 | 318 | quarterly obs x quarterly vintages | same as above |
| `philfed_rtdsm/cpiQvMd.xlsx` | https://www.philadelphiafed.org/-/media/FRBP/Assets/Surveys-And-Data/real-time-data/data-files/xlsx/cpiQvMd.xlsx | `57d28f99b28ca9a37801fcdd5026fae9b859e58b0f3dc1e150a55c544598bc34` | 1947:01..2026:07 | 955 | monthly obs x quarterly vintages | CPI-U index, SA |
| `philfed_rtdsm/employMvMd.xlsx` | https://www.philadelphiafed.org/-/media/FRBP/Assets/Surveys-And-Data/real-time-data/data-files/xlsx/employMvMd.xlsx | `a5cab543e1dcd135a2339b10ce0d6d920d23ad5a43c35cc97eca678914dd4fef` | 1939:01..2026:08 | 1052 | monthly obs x monthly vintages | thousands of persons, SA |
| `philfed_rtdsm/employ_level_first_second_third.xlsx` | https://www.philadelphiafed.org/-/media/FRBP/Assets/Surveys-And-Data/real-time-data/data-files/xlsx/employ_level_first_second_third.xlsx | `9db563b4cb32feb7e69af18da2ed4cd2fe7e440fd2e996aafbca2800d24a0c3e` | 1964:11..2026:08 | 742 | monthly | M/M change in thousands, first/second/third releases |
| `philfed_rtdsm/iptMvMd.xlsx` | https://www.philadelphiafed.org/-/media/FRBP/Assets/Surveys-And-Data/real-time-data/data-files/xlsx/iptMvMd.xlsx | `89ac73de4144749bf8ef2ce47314da8448ecb235f7f369c32465be1588ea5a97` | 1919:01..2026:08 | 1292 | monthly obs x monthly vintages | IP total index (base year varies by vintage) |
| `philfed_rtdsm/ipt_first_second_third.xlsx` | https://www.philadelphiafed.org/-/media/FRBP/Assets/Surveys-And-Data/real-time-data/data-files/xlsx/ipt_first_second_third.xlsx | `3f721ca133dedee1d5f8258464777979d6aa8237cad18b747c54b1023210cdb0` | 1962:10..2026:08 | 767 | monthly | IP first/second/third releases |
| `philfed_rtdsm/routputMvQd.xlsx` | https://www.philadelphiafed.org/-/media/FRBP/Assets/Surveys-And-Data/real-time-data/data-files/xlsx/routputMvQd.xlsx | `2be1c0f4f902df478adbc429c73fadfe6c76e5a85d28405c1a9877c2087233f6` | 1947:Q1..2026:Q2 | 318 | quarterly obs x monthly vintages | billions of real (chained) USD, SAAR; base year varies by vintage |
| `philfed_rtdsm/routput_first_second_third.xlsx` | https://www.philadelphiafed.org/-/media/FRBP/Assets/Surveys-And-Data/real-time-data/data-files/xlsx/routput_first_second_third.xlsx | `2bffa7a68ad43a950a04cb378a368b5e59192b1febcfe22d2a0e110132bfc9c5` | 1965:Q3..2026:Q2 | 244 | quarterly | annualized q/q growth %, first/second/third releases |
| `philfed_rtdsm/rucQvMd.xlsx` | https://www.philadelphiafed.org/-/media/FRBP/Assets/Surveys-And-Data/real-time-data/data-files/xlsx/rucQvMd.xlsx | `d971e59d3ed5f1322a46631743508fb1ad5eee39bfbe12425a641a277fdd9b9a` | 1947:01..2026:07 | 955 | monthly obs x quarterly vintages | %, SA |
| `schwert/STKDATD.DAT` | https://www.billschwert.com/stkdatd.zip (unzipped) | `4b052585e1dfc146eb3c2fcdf71664ed85e264920b983b6d131971190f2bd451` | 18850217..19620702 | 22474 | daily | decimal: total return, capital gain return, dividend yield |
| `schwert/STKDATM.DAT` | https://www.billschwert.com/stkdatm.zip (unzipped) | `64c8f93494ee2a5e1c539162068ca6f89b1a40b0194df30bd1371feabd132205` | 180201..192512 | 1488 | monthly | decimal: return, capital gain, div yield, unadjusted capital return |
| `schwert/zips/stkdatd.zip` | https://www.billschwert.com/stkdatd.zip | `34841bb769160902e088b3cfe4ed34704cd1190db2811024f8f01fce03f71289` | - | - | - | original zip |
| `schwert/zips/stkdatm.zip` | https://www.billschwert.com/stkdatm.zip | `a58769c080d463a5a1d963e1a1ebdb2aec8541f9e0a6be1d39d2cb4fc70b1b6e` | - | - | - | original zip |
| `shiller/ie_data.xls` | https://img1.wsimg.com/blobby/go/e5e77e0b-59d1-44d9-ab25-4763ac982e53/downloads/1449043e-a1ed-4e2e-8e9c-7b9a2a064493/ie_data.xls?ver=1791297298731 (linked from https://shillerdata.com/) | `98a54927942e842ec07ffe73000998e793953708c345b6b27bb363e9ada8366a` | 1871-01..2026-10 | 1870 | monthly | P/D/E nominal USD, CPI index, GS10 %, real series in current-month USD, CAPE ratio |
| `shiller/ie_data_yale_stale.xls` | http://www.econ.yale.edu/~shiller/data/ie_data.xls | `0df9392b7dacf91f756e92c8db508ad903c4588b43f3253680eec3dd8b40db68` | 1871-01..2023-09 | 1833 | monthly | stale copy, same layout |
| `treasury/feds200628.csv` | https://www.federalreserve.gov/data/yield-curve-tables/feds200628.csv | `2ebdb0a0e94c586445ab9255c7c2d4809f2cdb3776493388453ebb9587ec4342` | 1961-06-14..2026-10-02 | 17038 | daily | % continuously compounded zero yields (SVENY), par yields (SVENPY), forwards, NSS params |
| `treasury/histretSP.xls` | https://www.stern.nyu.edu/~adamodar/pc/datasets/histretSP.xls (redirects to pages.stern.nyu.edu) | `28b8110916a15a4dcc11c87c6422510704608ddedcdfa67a1298abdc22e49c69` | 1928..2025 | 98 | annual | % annual total returns (S&P, 3m bill, 10y T-bond, Baa, real estate, gold) |

## check_raw_data.py output (2026-10-08)

Run: `python3 scripts/check_raw_data.py` (needs pandas, openpyxl, xlrd).

| file | sheet/series | first | last | rows | notes |
|---|---|---|---|---|---|
| fred/AAA.csv | AAA | 1919-01-01 | 2026-09-01 | 1293 |  |
| fred/ANFCI.csv | ANFCI | 1971-01-08 | 2026-10-02 | 2909 |  |
| fred/BAA.csv | BAA | 1919-01-01 | 2026-09-01 | 1293 |  |
| fred/BAMLC0A0CM.csv | BAMLC0A0CM | 2023-10-09 | 2026-10-06 | 784 | 9 blank obs |
| fred/BAMLH0A0HYM2.csv | BAMLH0A0HYM2 | 2023-10-09 | 2026-10-06 | 785 | 8 blank obs |
| fred/CPIAUCSL.csv | CPIAUCSL | 1947-01-01 | 2026-08-01 | 955 | 1 blank obs |
| fred/DAAA.csv | DAAA | 1983-01-03 | 2026-10-06 | 10986 | 431 blank obs |
| fred/DBAA.csv | DBAA | 1986-01-02 | 2026-10-06 | 10227 | 407 blank obs |
| fred/DCOILWTICO.csv | DCOILWTICO | 1986-01-02 | 2026-10-06 | 9517 | 1117 blank obs |
| fred/DGS10.csv | DGS10 | 1962-01-02 | 2026-10-06 | 16176 | 720 blank obs |
| fred/DGS2.csv | DGS2 | 1976-06-01 | 2026-10-06 | 12584 | 552 blank obs |
| fred/DTB3.csv | DTB3 | 1954-01-04 | 2026-10-06 | 18182 | 800 blank obs |
| fred/DTWEXBGS.csv | DTWEXBGS | 2006-01-02 | 2026-10-02 | 5203 | 212 blank obs |
| fred/FEDFUNDS.csv | FEDFUNDS | 1954-07-01 | 2026-09-01 | 867 |  |
| fred/GS1.csv | GS1 | 1953-04-01 | 2026-09-01 | 882 |  |
| fred/GS10.csv | GS10 | 1953-04-01 | 2026-09-01 | 882 |  |
| fred/ICSA.csv | ICSA | 1967-01-07 | 2026-09-26 | 3117 |  |
| fred/INDPRO.csv | INDPRO | 1919-01-01 | 2026-08-01 | 1292 |  |
| fred/M2SL.csv | M2SL | 1959-01-01 | 2026-08-01 | 812 |  |
| fred/NFCI.csv | NFCI | 1971-01-08 | 2026-10-02 | 2909 |  |
| fred/PAYEMS.csv | PAYEMS | 1939-01-01 | 2026-09-01 | 1053 |  |
| fred/STLFSI4.csv | STLFSI4 | 1993-12-31 | 2026-10-02 | 1710 |  |
| fred/T10Y2Y.csv | T10Y2Y | 1976-06-01 | 2026-10-07 | 12585 | 552 blank obs |
| fred/T10Y3M.csv | T10Y3M | 1982-01-04 | 2026-10-07 | 11194 | 484 blank obs |
| fred/TB3MS.csv | TB3MS | 1934-01-01 | 2026-09-01 | 1113 |  |
| fred/TEDRATE.csv | TEDRATE | 1986-01-02 | 2022-01-21 | 8853 | 554 blank obs |
| fred/UMCSENT.csv | UMCSENT | 1952-11-01 | 2026-08-01 | 676 | 210 blank obs |
| fred/UNRATE.csv | UNRATE | 1948-01-01 | 2026-09-01 | 944 | 1 blank obs |
| fred/USREC.csv | USREC | 1854-12-01 | 2026-09-01 | 2062 |  |
| fred/USRECM.csv | USRECM | 1854-12-01 | 2026-09-01 | 2062 |  |
| fred/VIXCLS.csv | VIXCLS | 1990-01-02 | 2026-10-06 | 9289 | 302 blank obs |
| fred/VXOCLS.csv | VXOCLS | 1986-01-02 | 2021-09-23 | 9002 | 319 blank obs |
| french/10_Industry_Portfolios.csv | block1 (monthly) | 192607 | 202608 | 1202 | 8 data blocks (4 annual) |
| french/Asia_Pacific_ex_Japan_3_Factors.csv | block1 (monthly) | 199007 | 202608 | 434 | 2 data blocks (1 annual) |
| french/Developed_3_Factors.csv | block1 (monthly) | 199007 | 202608 | 434 | 2 data blocks (1 annual) |
| french/Developed_3_Factors_Daily.csv | block1 (daily) | 19900702 | 20260831 | 9436 | 1 data blocks (0 annual) |
| french/Developed_MOM_Factor.csv | block1 (monthly) | 199011 | 202608 | 430 | 2 data blocks (1 annual) |
| french/Developed_ex_US_3_Factors.csv | block1 (monthly) | 199007 | 202608 | 434 | 2 data blocks (1 annual) |
| french/Developed_ex_US_3_Factors_Daily.csv | block1 (daily) | 19900702 | 20260831 | 9436 | 1 data blocks (0 annual) |
| french/Developed_ex_US_MOM_Factor.csv | block1 (monthly) | 199011 | 202608 | 430 | 2 data blocks (1 annual) |
| french/Emerging_5_Factors.csv | block1 (monthly) | 198907 | 202608 | 446 | 2 data blocks (1 annual) |
| french/Europe_3_Factors.csv | block1 (monthly) | 199007 | 202608 | 434 | 2 data blocks (1 annual) |
| french/F-F_Momentum_Factor.csv | block1 (monthly) | 192701 | 202608 | 1196 | 2 data blocks (1 annual) |
| french/F-F_Momentum_Factor_daily.csv | block1 (daily) | 19261103 | 20260831 | 26216 | 1 data blocks (0 annual) |
| french/F-F_Research_Data_Factors.csv | block1 (monthly) | 192607 | 202608 | 1202 | 2 data blocks (1 annual) |
| french/F-F_Research_Data_Factors_daily.csv | block1 (daily) | 19260701 | 20260831 | 26317 | 1 data blocks (0 annual) |
| french/Japan_3_Factors.csv | block1 (monthly) | 199007 | 202608 | 434 | 2 data blocks (1 annual) |
| french/North_America_3_Factors.csv | block1 (monthly) | 199007 | 202608 | 434 | 2 data blocks (1 annual) |
| goyal/GW2008_PredictorData_updated_2025.xlsx | Monthly | 187101 | 202512 | 1860 | CRSP_SPvw non-missing 192601-202512 |
| goyal/GW2008_PredictorData_updated_2025.xlsx | Quarterly | 18711 | 20254 | 620 | CRSP_SPvw non-missing 19261-20254 |
| goyal/GW2008_PredictorData_updated_2025.xlsx | Annual | 1871 | 2025 | 155 | CRSP_SPvw non-missing 1926-2025 |
| goyal/GWZ2024_GW2008_alldata_2025.xlsx | Monthly | 187101 | 202512 | 1860 | ret non-missing 192601-202512 |
| goyal/GWZ2024_GW2008_alldata_2025.xlsx | Quarterly | 18711 | 20254 | 620 | ret non-missing 19261-20254 |
| goyal/GWZ2024_GW2008_alldata_2025.xlsx | Annual | 1871 | 2025 | 155 | ret non-missing 1926-2025 |
| goyal/GWZ2024_data_2025_csv.zip | 46 csv (unextracted) | 1926 | 2025 | 100 | sample member gip_A.csv: rows=obs year, cols=vintage/forecast-origin |
| shiller/ie_data.xls | Data | 1871-01 | 2026-10 | 1870 |  |
| shiller/ie_data_yale_stale.xls | Data | 1871-01 | 2023-09 | 1833 |  |
| philfed_rtdsm/ROUTPUTQvQd.xlsx | ROUTPUT | 1947:Q1 | 2026:Q2 | 318 | 244 vintages ROUTPUT65Q4..ROUTPUT26Q3 |
| philfed_rtdsm/cpiQvMd.xlsx | cpi | 1947:01 | 2026:07 | 955 | 244 vintages CPI65Q4..CPI26Q3 |
| philfed_rtdsm/employMvMd.xlsx | employ | 1939:01 | 2026:08 | 1052 | 742 vintages EMPLOY64M12..EMPLOY26M9 |
| philfed_rtdsm/employ_level_first_second_third.xlsx | DATA | 1964:11 | 2026:08 | 742 | first/second/third release table |
| philfed_rtdsm/iptMvMd.xlsx | ipt | 1919:01 | 2026:08 | 1292 | 767 vintages IPT62M11..IPT26M9 |
| philfed_rtdsm/ipt_first_second_third.xlsx | DATA | 1962:10 | 2026:08 | 767 | first/second/third release table |
| philfed_rtdsm/routputMvQd.xlsx | routput | 1947:Q1 | 2026:Q2 | 318 | 732 vintages ROUTPUT65M11..ROUTPUT26M10 |
| philfed_rtdsm/routput_first_second_third.xlsx | DATA | 1965:Q3 | 2026:Q2 | 244 | first/second/third release table |
| philfed_rtdsm/rucQvMd.xlsx | ruc | 1947:01 | 2026:07 | 955 | 244 vintages RUC65Q4..RUC26Q3 |
| jst/JSTdatasetR6.xlsx | Sheet1 | 1870 | 2020 | 2718 | 18 countries; eq_tr non-missing to 2020 |
| jst/JSTdatasetR6.dta | stata | 1870 | 2020 | 2718 | 59 vars |
| aqr/Betting-Against-Beta-Equity-Factors-Daily.xlsx | BAB Factors | 1930-12-01 | 2026-07-31 | 25369 |  |
| aqr/Betting-Against-Beta-Equity-Factors-Daily.xlsx | MKT | 1926-07-01 | 2026-07-31 | 26678 |  |
| aqr/Betting-Against-Beta-Equity-Factors-Daily.xlsx | SMB | 1926-07-01 | 2026-07-31 | 26678 |  |
| aqr/Betting-Against-Beta-Equity-Factors-Daily.xlsx | HML FF | 1926-07-01 | 2026-07-31 | 26678 |  |
| aqr/Betting-Against-Beta-Equity-Factors-Daily.xlsx | HML Devil | 1926-07-01 | 2026-07-31 | 26678 |  |
| aqr/Betting-Against-Beta-Equity-Factors-Daily.xlsx | UMD | 1927-01-03 | 2026-07-31 | 26528 |  |
| aqr/Betting-Against-Beta-Equity-Factors-Daily.xlsx | RF | 1926-07-31 | 2026-08-31 | 27266 |  |
| aqr/Betting-Against-Beta-Equity-Factors-Monthly.xlsx | BAB Factors | 1930-12-31 | 2026-07-31 | 1148 |  |
| aqr/Betting-Against-Beta-Equity-Factors-Monthly.xlsx | MKT | 1926-07-31 | 2026-07-31 | 1201 |  |
| aqr/Betting-Against-Beta-Equity-Factors-Monthly.xlsx | SMB | 1926-07-31 | 2026-07-31 | 1201 |  |
| aqr/Betting-Against-Beta-Equity-Factors-Monthly.xlsx | HML FF | 1926-07-31 | 2026-07-31 | 1201 |  |
| aqr/Betting-Against-Beta-Equity-Factors-Monthly.xlsx | HML Devil | 1926-07-31 | 2026-07-31 | 1201 |  |
| aqr/Betting-Against-Beta-Equity-Factors-Monthly.xlsx | UMD | 1927-01-31 | 2026-07-31 | 1195 |  |
| aqr/Betting-Against-Beta-Equity-Factors-Monthly.xlsx | ME(t-1) | 1926-07-31 | 2026-08-31 | 1202 |  |
| aqr/Betting-Against-Beta-Equity-Factors-Monthly.xlsx | RF | 1926-07-31 | 2026-08-31 | 1202 |  |
| aqr/Century-of-Factor-Premia-Monthly.xlsx | Century of Factor Premia | 1926-07-30 | 2026-02-27 | 1196 |  |
| aqr/Commodities-for-the-Long-Run-Index-Level-Data-Monthly.xlsx | Commodities for the Long Run | 1877-02-28 | 2025-05-30 | 1780 |  |
| aqr/Credit-Risk-Premium-Preliminary-Paper-Data.xlsx | Credit Risk Premium | 1926-01-29 | 2014-12-31 | 1068 |  |
| aqr/Quality-Minus-Junk-Factors-Daily.xlsx | QMJ Factors | 1957-07-01 | 2026-07-31 | 17769 |  |
| aqr/Quality-Minus-Junk-Factors-Daily.xlsx | MKT | 1926-07-01 | 2026-07-31 | 26678 |  |
| aqr/Quality-Minus-Junk-Factors-Daily.xlsx | SMB | 1926-07-01 | 2026-07-31 | 26678 |  |
| aqr/Quality-Minus-Junk-Factors-Daily.xlsx | HML FF | 1926-07-01 | 2026-07-31 | 26678 |  |
| aqr/Quality-Minus-Junk-Factors-Daily.xlsx | HML Devil | 1926-07-01 | 2026-07-31 | 26678 |  |
| aqr/Quality-Minus-Junk-Factors-Daily.xlsx | UMD | 1927-01-03 | 2026-07-31 | 26528 |  |
| aqr/Quality-Minus-Junk-Factors-Daily.xlsx | RF | 1926-07-31 | 2026-08-31 | 27266 |  |
| aqr/Quality-Minus-Junk-Factors-Monthly.xlsx | QMJ Factors | 1957-07-31 | 2026-07-31 | 829 |  |
| aqr/Quality-Minus-Junk-Factors-Monthly.xlsx | MKT | 1926-07-31 | 2026-07-31 | 1201 |  |
| aqr/Quality-Minus-Junk-Factors-Monthly.xlsx | SMB | 1926-07-31 | 2026-07-31 | 1201 |  |
| aqr/Quality-Minus-Junk-Factors-Monthly.xlsx | HML FF | 1926-07-31 | 2026-07-31 | 1201 |  |
| aqr/Quality-Minus-Junk-Factors-Monthly.xlsx | HML Devil | 1926-07-31 | 2026-07-31 | 1201 |  |
| aqr/Quality-Minus-Junk-Factors-Monthly.xlsx | UMD | 1927-01-31 | 2026-07-31 | 1195 |  |
| aqr/Quality-Minus-Junk-Factors-Monthly.xlsx | ME(t-1) | 1926-07-31 | 2026-08-31 | 1202 |  |
| aqr/Quality-Minus-Junk-Factors-Monthly.xlsx | RF | 1926-07-31 | 2026-08-31 | 1202 |  |
| aqr/Time-Series-Momentum-Factors-Monthly.xlsx | TSMOM Factors | 1985-01-31 | 2026-05-29 | 497 |  |
| aqr/Value-and-Momentum-Everywhere-Factors-Monthly.xlsx | VME Factors | 1972-01-31 | 2026-07-31 | 655 |  |
| treasury/feds200628.csv | GSW daily | 1961-06-14 | 2026-10-02 | 17038 | SVENY10 non-missing 1971-08-16..2026-10-02; SVENY30 from 1985-11-25 |
| treasury/histretSP.xls | Returns by year | 1928 | 2025 | 98 | annual |
| schwert/STKDATD.DAT | daily | 18850217 | 19620702 | 22474 |  |
| schwert/STKDATM.DAT | monthly | 180201 | 192512 | 1488 |  |
| `french/Europe_3_Factors_Daily.csv` | https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/Europe_3_Factors_Daily_CSV.zip (unzipped; added 2026-10-08) | `5178bce67798f86c9e1741aac7d97bc77334bda4096d60944bbe4846dc99be72` | 19900702..20260831 | daily | % per period |
| `french/Japan_3_Factors_Daily.csv` | https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/Japan_3_Factors_Daily_CSV.zip (unzipped; added 2026-10-08) | `a5afa8f15d2a377eaa17eb131208a9e8c735063b1710d610a4e4c4d000c4ee79` | 19900702..20260831 | daily | % per period |
| `french/Asia_Pacific_ex_Japan_3_Factors_Daily.csv` | https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/Asia_Pacific_ex_Japan_3_Factors_Daily_CSV.zip (unzipped; added 2026-10-08) | `4d5d7c2dc4fef64824b6b59296f0610bf3e514778fd73ecd0412bb65966333cc` | 19900702..20260831 | daily | % per period |
| `french/North_America_3_Factors_Daily.csv` | https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/North_America_3_Factors_Daily_CSV.zip (unzipped; added 2026-10-08) | `0295abe81dc29f8450e6a2aebe307d219791ce3e1393da9e1191151832b50fe2` | 19900702..20260831 | daily | % per period |

# Data Sources

Use the public UCI dataset at https://doi.org/10.24432/C5MC89 and retain its attribution. The dataset is not bundled in the Week 1 submission.

The public documents used for definitions and the reference guide are listed in [the project scope](../docs/week1_project_scope.md). Record download dates and dataset checksums when implementation begins. Do not add personal records, credentials, or the signed FYP proposal to this repository.

## Public PDF documents for Topic 2 and Topic 3 preparation

Two domain PDFs are included, downloaded from the publisher on 5 November 2026. Both are unmodified open-access articles under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); copyright remains with the authors. They support the reference guide and feature definitions, not additional labelled training data.

| Local file | Attribution and canonical source | Download URL | Pages |
| --- | --- | --- | --- |
| [realinho_2022.pdf](realinho_2022.pdf) | Realinho, V., Machado, J., Baptista, L., & Martins, M. V. (2022). Predicting Student Dropout and Academic Success. Data, 7(11), 146. https://doi.org/10.3390/data7110146 | https://www.mdpi.com/2306-5729/7/11/146/pdf | 17 |
| [martins_2023.pdf](martins_2023.pdf) | Martins, M. V., Baptista, L., Machado, J., & Realinho, V. (2023). Multi-Class Phased Prediction of Academic Performance and Dropout in Higher Education. Applied Sciences, 13(8), 4702. https://doi.org/10.3390/app13084702 | https://www.mdpi.com/2076-3417/13/8/4702/pdf | 15 |

SHA-256 checksums of the stored PDF bytes:

```text
realinho_2022.pdf  1be95db77df7714e2b0783811c414895150c45cee6bbd8a79d6bd61b3a2185fb
martins_2023.pdf   2f092cb9803c2ae1f3a9198f9fe3752c3f664c0f5307b2177417a8c057d4ab46
```

Initial parsing observations: both first pages include a citation/licence sidebar as well as the article text. Plain extraction can put sidebar content before the title, split a DOI across lines, and retain ligatures or line-break hyphenation. Later PDF processing should preserve page references, separate boilerplate from substantive content, and check table reading order. No automated PDF parsing pipeline or Colab setup is claimed in Week 2.
